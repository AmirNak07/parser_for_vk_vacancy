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

    Создать файл ".env" и заполнить его по примеру из файла ".env.example" (Нужно скопировать только те строки, которые НЕ начинаются с "#"). Пример файла ".env", если мы используем Chrome:

    ```env
    ID_TABLE = "fal;lajf_alsfll_flasljaf-afs12k"
    SPREADSHEET = "ВК"
    ```

6. Создать файл аутенфикации OAuth

    В директорию с проектом переместите(скопируете) файл с вашими данными из Google Workplace с вашим проектом и назовите "credentials.json"

## Запуск

```bash
python main.py
```

[©Amir Nakhushev](https://github.com/AmirNak07)
