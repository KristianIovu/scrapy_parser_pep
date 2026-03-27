import scrapy

from pep_parse.items import PepParseItem


PEP_DOMAIN = "peps.python.org"
START_URLS = [f"https://{PEP_DOMAIN}/"]


class PepSpider(scrapy.Spider):
    """Паук для парсинга PEP."""

    name = "pep"
    allowed_domains = [PEP_DOMAIN]
    start_urls = START_URLS

    def parse(self, response):
        """Парсит индекс и собирает ссылки на PEP."""
        pep_links = response.css('a[href^="pep-"]::attr(href)').getall()

        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсит страницу PEP."""
        title = response.css('h1.page-title::text').get()

        number = title.split()[0].replace('PEP', '').strip()
        name = ' '.join(title.split()[1:]).strip()

        status = response.css('dt:contains("Status") + dd::text').get()

        status = status.strip() if status else 'Unknown'

        yield PepParseItem(
            number=number,
            name=name,
            status=status
        )
