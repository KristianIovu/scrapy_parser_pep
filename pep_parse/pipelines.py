import csv
from datetime import datetime, timezone
from pathlib import Path


class PepParsePipeline:
    """Pipeline для подсчета статусов  PEP и сохранения результатов."""

    def open_spider(self, spider):
        """Инициализация словаря и списка при запуске паука."""
        self.status_count = {}
        self.pep_items = []

    def process_item(self, item, spider):
        """Подсчет количества статусов и сохранение PEP."""
        status = item.get('status')
        self.status_count[status] = (self.status_count.get(status, 0) + 1)
        self.pep_items.append(item)
        return item

    def close_spider(self, spider):
        """Запись значений в файлы."""
        # Получает настройки FEEDS из паука
        feeds = spider.crawler.settings.getdict('FEEDS') or {}

        # Определяет директорию для сохранения
        if feeds:
            feed_path = list(feeds.keys())[0]
            if isinstance(feed_path, Path):
                results_dir = feed_path.parent
            else:
                results_dir = Path(str(feed_path)).parent
        else:
            results_dir = Path.cwd() / 'results'

        # Создаёт папку
        results_dir.mkdir(parents=True, exist_ok=True)

        current_dt = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')

        # Сохраняет файл PEP
        pep_filename = results_dir / f'pep_{current_dt}.csv'
        with open(pep_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['number', 'name', 'status'])
            for item in self.pep_items:
                writer.writerow([item['number'], item['name'], item['status']])

        # Сохраняет сводку
        summary_filename = results_dir / f'status_summary_{current_dt}.csv'
        result = [('Статус', 'Количество')]
        result.extend(self.status_count.items())
        result.append(('Total', sum(self.status_count.values())))

        with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(result)
