import scrapy


class PepParseItem(scrapy.Item):
    """Класс для хранения данных о PEP."""

    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
