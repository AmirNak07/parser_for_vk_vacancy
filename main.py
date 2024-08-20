import asyncio
import time
import json

import aiohttp
import httpx


def get_opened_projects(link: str) -> list:
    vacancy_request = httpx.get(link)
    if vacancy_request.status_code == 200:
        vacancy_html = vacancy_request.text

    vacancy_all_json = json.loads(vacancy_html[vacancy_html.find('<script id="__NEXT_DATA__"'):].replace('<script id="__NEXT_DATA__" type="application/json">', "").replace("</script></body></html>", ""))
    vacancy_json = vacancy_all_json["props"]["pageProps"]["page"]["vacancies"]
    vacancy_opened = [vacancy["id"] for vacancy in vacancy_json if vacancy["is_opened"]]
    print(vacancy_opened)
    print("-" * 20)
    return vacancy_opened


def remove_non_breaking_spaces(data: dict) -> dict:
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = remove_non_breaking_spaces(value)
    elif isinstance(data, list):
        data = [remove_non_breaking_spaces(item) for item in data]
    elif isinstance(data, str):
        data = data.replace('\xa0', ' ')
    elif isinstance(data, int) or data is None:
        data = data

    return data


async def get_projects(vacancy_id: int, session: aiohttp.ClientSession) -> list:
    link = f"https://internship.vk.company/vacancy/{vacancy_id}"
    async with session.get(link) as response:
        vacancy_html = await response.text("utf-8")
    vacancy_all_json = json.loads(vacancy_html[vacancy_html.find('<script id="__NEXT_DATA__"'):].replace('<script id="__NEXT_DATA__" type="application/json">', "").replace("</script></body></html>", ""))
    vacancy_json = remove_non_breaking_spaces(vacancy_all_json["props"]["pageProps"]["page"]["vacancy"])
    vacancy_result = [
        vacancy_json["title"],
        vacancy_json["business_unit"]["name"],
        vacancy_json["city"],
        vacancy_json["format"],
        vacancy_json["employment"],
        "\n".join(vacancy_json["landing"]["aboutTasksText"]),
        "\n".join(vacancy_json["landing"]["aboutSkillsText"]["items"]),
        f"https://internship.vk.company/vacancy/{vacancy_json['id']}",
        "Стажировка" if vacancy_json["internship_type"] == "internship" else "Вакансия"
    ]

    return vacancy_result


async def download_all_vacancy() -> None:
    vacancy_link = "https://internship.vk.company/vacancy"
    internship_link = "https://internship.vk.company/internship"

    vacancy_id_list = get_opened_projects(vacancy_link)
    internship_id_list = get_opened_projects(internship_link)

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_projects(i, session)) for i in vacancy_id_list]
        tasks.extend([asyncio.create_task(get_projects(i, session)) for i in internship_id_list])

        result = await asyncio.gather(*tasks)
        return result


async def main():
    result = await download_all_vacancy()
    print(result)
    return result

if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    print(f"Время работы программы: {time.time() - t0}")
