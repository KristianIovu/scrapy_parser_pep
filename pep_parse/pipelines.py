import csv
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    """Сохранение статистики по статусам PEP."""

    def open_spider(self, spider):
        """Инициализация счётчика статусов и нормализация FEEDS."""
        self.status_count = {}

        feeds = spider.settings.get('FEEDS')

        if feeds:
            normalized_feeds = {}

            for uri, opts in feeds.items():
                # Преобразование Path в строку, если необходимо
                normalized_feeds[str(uri)] = opts

            spider.settings.set('FEEDS', normalized_feeds)

    def process_item(self, item, spider):
        """Подсчёт количества PEP по статусам."""
        status = item.get('status')
        self.status_count[status] = self.status_count.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        """Создание итоговых CSV-файлов со статистикой."""
        feeds = spider.settings.get('FEEDS')

        # Определение директории и шаблона имени файла
        if feeds:
            feed_uri = list(feeds.keys())[0]

            if isinstance(feed_uri, Path):
                results_dir = feed_uri.parent
                pep_filename_template = feed_uri.name
            else:
                feed_path = Path(feed_uri)
                results_dir = feed_path.parent
                pep_filename_template = feed_path.name
        else:
            results_dir = Path('results')
            pep_filename_template = 'pep_%(time)s.csv'

        # Создание директории для результатов
        results_dir.mkdir(parents=True, exist_ok=True)

        # Генерация временной метки для имени файла
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Создание файла pep_*.csv, если Scrapy не создал его автоматически
        pep_filename = pep_filename_template.replace('%(time)s', timestamp)
        pep_file = results_dir / pep_filename

        if not pep_file.exists():
            with open(pep_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['number', 'name', 'status'])

        # Создание файла status_summary_*.csv со статистикой по статусам
        summary_file = results_dir / f'status_summary_{timestamp}.csv'

        # Сортировка статусов для упорядоченного вывода
        sorted_statuses = sorted(self.status_count.items())
        total = sum(self.status_count.values())

        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])

            for status, count in sorted_statuses:
                writer.writerow([status, count])

            writer.writerow(['Total', total])
