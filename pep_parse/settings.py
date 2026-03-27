import os
from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

# Папки для результатов и логов
RESULT_DIR = Path('results')
LOGS_DIR = BASE_DIR / 'logs'

# Создание директорий
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

BOT_NAME = "pep_parse"

# Константа для модуля пауков
SPIDER_MODULE = "pep_parse.spiders"

SPIDER_MODULES = [SPIDER_MODULE]
NEWSPIDER_MODULE = SPIDER_MODULE

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1

FEED_EXPORT_ENCODING = 'utf-8'

FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
