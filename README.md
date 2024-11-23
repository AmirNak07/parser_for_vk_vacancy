# Парсер ВК вакансий и стажировок

## Описание

Данный код парсит форумы с открытой регистрацией из сайтов ВК: [вакансии](https://internship.vk.company/vacancy), [стажировки](https://internship.vk.company/internship) и отправляет в Google Sheets.

## Установка

1. Склонировать репозиторий

    ```bash
    git clone link_to_repository
    ```

    Далее переходим в директорию с проектом. Рекомендуется использовать виртуальное окружение Python(virtualvenv). Если вы используете глобальный интерпретатор, то этапы 2-3 можете пропустить

2. Создание виртуального окржения

    ```bash
    python3.12 -m venv .venv
    ```

    Возможно использовать другие версии(я использовал 3.12.3)

3. Активация виртуального окружения

    Для Windows:

    ```powershell
    .venv\Scripts\activate
    ```

    Для Linux/Mac OS:

    ```bash
    source .venv/bin/activate
    ```

4. Подтянуть все зависимости

    ```bash
    pip install -r requirements.txt
    ```

5. Настроить перменные среды

    Создать файл ".env" в папке "config" и заполнить его по примеру из файла ".env.example" (Нужно скопировать только те строки, которые НЕ начинаются с "#").

    ```env
    ID_TABLE = "fal;lajf_alsfll_flasljaf-afs12k"
    SPREADSHEET = "ВК"
    ```

6. Создать файл аутенфикации OAuth

    В директорию "config" переместите(скопируете) файл с вашими данными из Google Workplace из вашего проекта и назовите "credentials.json"

## Запуск(обычный)

```bash
python main.py
```

## Запуск(Docker)

1. Собрать образ:

    ```bash
    docker build -t vk_parser_image .
    ```

2. Запустить контейнер

    ```bash
    docker run -d --name vk_parser vk_parser_image
    ```

[©Amir Nakhushev](https://github.com/AmirNak07)
