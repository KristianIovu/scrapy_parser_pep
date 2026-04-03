# scrapy_parser_pep

Асинхронный парсер документов Python Enhancement Proposals (PEP) на базе фреймворка Scrapy.

## Описание

Парсер собирает информацию о всех PEP с сайта [peps.python.org](https://peps.python.org/) и сохраняет её в два CSV-файла:
- `pep_ДатаВремя.csv` — список всех PEP с номерами, названиями и статусами
- `status_summary_ДатаВремя.csv` — сводка по статусам PEP с общим количеством

## Технологии

- Python 3.12
- Scrapy 2.10
- pytest 8.3

## Установка и запуск

1. Клонировать репозиторий:
git clone https://github.com/KristianIovu/scrapy_parser_pep.git
cd scrapy_parser_pep

2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/Scripts/activate

3. Установить зависимости
pip install -r requirements.txt

4. Запустить парсер
cd src
scrapy crawl pep

## Результат
В папке result появятся два файла:
1. pep_20241215_120000.csv
2. status_summary_20241215_120000.csv
