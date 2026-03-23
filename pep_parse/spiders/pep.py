import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Паук для парсинга."""

    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        """Собирает ссылки на документы PEP."""
        pep_links = response.css('a[href^="pep-"]::attr(href)').getall()
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсит страницу документа PEP."""
        # Извлекает номер PEP из заголовка
        title = response.css('h1.page-title::text').get()
        number = title.split()[0].replace('PEP', '').strip()

        # Извлекает название PEP
        name = ' '.join(title.split()[1:]).strip()

        # Извлекает статус, использует селектор для элемента, след. за Status
        status = response.css('dt:contains("Status") + dd::text').get()
        if status:
            status = status.strip()
        else:
            status = 'Unknown'

        yield PepParseItem(
            number=number,
            name=name,
            status=status
        )
