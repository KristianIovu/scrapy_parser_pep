import csv
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    """Pipeline для подсчета статусов PEP и сохранения CSV."""

    def open_spider(self, spider):
        """Выполняется при открывании паука."""
        # Счетчик статусов
        self.status_count = {}

        # Определяем директорию для результатов из FEEDS
        feeds = spider.settings.get('FEEDS')
        if feeds:
            feed_uri = list(feeds.keys())[0]
            self.results_dir = Path(feed_uri).parent
            # Имя шаблона pep-файла
            self.pep_filename_template = Path(feed_uri).name
        else:
            # Если FEEDS нет, fallback
            self.results_dir = Path('results')
            self.pep_filename_template = 'pep_%(time)s.csv'

        # Создаем директорию, если её нет
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        """Обрабатывает каждый элемент, полученный от паука."""
        status = item.get('status', 'Unknown')
        self.status_count[status] = self.status_count.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        """Выполняется при закрывании паука."""
        # Временная метка для файлов
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # pep_*.csv
        pep_file = self.results_dir / self.pep_filename_template.replace(
            '%(time)s', timestamp
        )
        if not pep_file.exists():
            with open(pep_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['number', 'name', 'status'])

        # status_summary_*.csv
        summary_file = self.results_dir / f'status_summary_{timestamp}.csv'
        total = sum(self.status_count.values())
        sorted_statuses = sorted(self.status_count.items())
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in sorted_statuses:
                writer.writerow([status, count])
            writer.writerow(['Total', total])
