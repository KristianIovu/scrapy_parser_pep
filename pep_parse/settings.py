import os
from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(BASE_DIR / 'results', exist_ok=True)

PEP_SPIDER_SETTINGS = {
    'name': 'pep',
    'allowed_domains': ['peps.python.org'],
    'start_urls': ['https://peps.python.org/'],
}

BOT_NAME = "pep_parse"
SPIDER_MODULES = ["pep_parse.spiders"]
NEWSPIDER_MODULE = "pep_parse.spiders"
TELNETCONSOLE_ENABLED = DEBUG

if not DEBUG:
    LOG_FILE = str(LOGS_DIR / 'scrapy.log')
    LOG_LEVEL = 'WARNING'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ROBOTSTXT_OBEY = True
COOKIES_ENABLED = True

CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
DNS_TIMEOUT = 10
DOWNLOAD_TIMEOUT = 30

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

HTTPCACHE_ENABLED = DEBUG
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = "httpcache"

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
