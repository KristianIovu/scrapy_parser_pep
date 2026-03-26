import os
from pathlib import Path


DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

os.makedirs(BASE_DIR / 'results', exist_ok=True)
os.makedirs(BASE_DIR / 'logs', exist_ok=True)


BOT_NAME = "pep_parse"

SPIDER_MODULES = ["pep_parse.spiders"]
NEWSPIDER_MODULE = "pep_parse.spiders"

ROBOTSTXT_OBEY = True


CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1


FEED_EXPORT_ENCODING = 'utf-8'


FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}


ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
