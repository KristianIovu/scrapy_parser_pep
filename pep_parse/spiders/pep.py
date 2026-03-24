import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Паук для парсинга PEP."""

    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        """Парсит индексную страницу и собирает ссылки на все документы PEP."""
        pep_links = response.css('a[href^="pep-"]::attr(href)').getall()
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсит страницу PEP и извлекает номер, название и статус."""
        title = response.css('h1.page-title::text').get()
        number = title.split()[0].replace('PEP', '').strip()
        name = ' '.join(title.split()[1:]).strip()
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
