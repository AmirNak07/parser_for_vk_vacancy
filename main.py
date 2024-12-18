import asyncio
import json
import time

import aiohttp
import gspread
import schedule
from gspread.client import Client as gspreadClient
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from config import NAME_WORKSHEET, TABLE_ID, LOGS_CONFIG


logger.remove()
logger.configure(**LOGS_CONFIG)


async def get_opened_projects(link: str, session: aiohttp.ClientSession) -> list:
    async with session.get(link) as response:
        if response.status == 200:
            vacancy_html = await response.text("utf-8")

    vacancy_all_json = json.loads(vacancy_html[vacancy_html.find('<script id="__NEXT_DATA__"'):].replace(
        '<script id="__NEXT_DATA__" type="application/json">', "").replace("</script></body></html>", ""))
    vacancy_json = vacancy_all_json["props"]["pageProps"]["page"]["vacancies"]
    vacancy_opened = [vacancy["id"]
                      for vacancy in vacancy_json if vacancy["is_opened"]]
    return vacancy_opened


async def remove_non_breaking_spaces(data: dict) -> dict:
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = await remove_non_breaking_spaces(value)
    elif isinstance(data, list):
        data = [await remove_non_breaking_spaces(item) for item in data]
    elif isinstance(data, str):
        data = data.replace('\xa0', ' ')
    elif isinstance(data, int) or data is None:
        data = data

    return data


async def get_projects(vacancy_id: int, session: aiohttp.ClientSession) -> list:
    link = f"https://internship.vk.company/vacancy/{vacancy_id}"
    async with session.get(link) as response:
        vacancy_html = await response.text("utf-8")
    vacancy_all_json = json.loads(vacancy_html[vacancy_html.find('<script id="__NEXT_DATA__"'):].replace(
        '<script id="__NEXT_DATA__" type="application/json">', "").replace("</script></body></html>", ""))
    vacancy_json = await remove_non_breaking_spaces(vacancy_all_json["props"]["pageProps"]["page"]["vacancy"])
    vacancy_result = [
        vacancy_json["title"],
        vacancy_json["business_unit"]["name"],
        vacancy_json["city"],
        vacancy_json["format"],
        vacancy_json["employment"],
        "\n".join(vacancy_json["landing"]["aboutTasksText"]["items"]),
        "\n".join(vacancy_json["landing"]["aboutSkillsText"]["items"]),
        f"https://internship.vk.company/vacancy/{vacancy_json['id']}",
        "Стажировка" if vacancy_json["internship_type"] == "internship" else "Вакансия",
        vacancy_json["direction"]
    ]

    return vacancy_result


async def download_all_vacancy() -> None:
    vacancy_link = "https://internship.vk.company/vacancy"
    internship_link = "https://internship.vk.company/internship"

    logger.debug("Поиск окткрытых вакансий...")
    async with aiohttp.ClientSession() as session:
        vacancy_id_list = await get_opened_projects(vacancy_link, session)
        internship_id_list = await get_opened_projects(internship_link, session)
    logger.debug(f"ID открытых вакансий: {vacancy_id_list + internship_id_list}")
    logger.debug("Сбор информации о вакансиях в таблицу...")
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_projects(i, session))
                 for i in vacancy_id_list]
        tasks.extend([asyncio.create_task(get_projects(i, session))
                     for i in internship_id_list])

        result = await asyncio.gather(*tasks)
        logger.debug("Таблица готова")
        return result


async def send_to_google_sheets(client: gspreadClient, table_id: str, worklist: str, data: list):
    logger.debug("Отправка таблицы в Google Sheets")
    titles = [["Позиция",
               "Команда",
               "Город",
               "Формат работы",
               "Занятость",
               "Предстоящие задачи",
               "Необходимо иметь",
               "Ссылка",
               "Раздел",
               "Направление"]]
    result_data = titles + data
    sheet = client.open_by_key(table_id)
    worksheet = sheet.worksheet(worklist)
    worksheet.clear()
    worksheet.append_rows(values=result_data)
    logger.info("Таблица отправлена")


@logger.catch
async def main():
    table_id = TABLE_ID
    name_worksheet = NAME_WORKSHEET

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "config/credentials.json", scope)
    client = gspread.authorize(creds)
    logger.info("Начало парсинга")
    vacancies = await download_all_vacancy()
    await send_to_google_sheets(client, table_id, name_worksheet, vacancies)
    logger.info("Парсинг прошёл успешно")


def timer():
    asyncio.run(main())


if __name__ == "__main__":
    # schedule.every().day.at("00:01", "Europe/Moscow").do(timer)
    schedule.every(3).hours.do(timer)
    while True:
        schedule.run_pending()
        time.sleep(1)
