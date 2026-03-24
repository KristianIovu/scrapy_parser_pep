import csv
from datetime import datetime, timezone
from pathlib import Path


class PepParsePipeline:
    """Pipeline для подсчёта статусов PEP и сохранения сводки."""

    def open_spider(self, spider):
        """Инициализация словаря и списка при запуске паука."""
        self.status_count = {}
        self.pep_items = []

    def process_item(self, item, spider):
        """Подсчёт количества статусов и сохранение PEP."""
        status = item.get('status')
        self.status_count[status] = self.status_count.get(status, 0) + 1
        self.pep_items.append(item)
        return item

    def close_spider(self, spider):
        """Сохранение файлов PEP и сводки по статусам."""
        # Получает настройки FEEDS из паука
        feeds = spider.crawler.settings.getdict('FEEDS') or {}

        # Определяет директорию для сохранения
        if feeds:
            feed_path = list(feeds.keys())[0]
            if isinstance(feed_path, Path):
                results_dir = feed_path.parent
            else:
                feed_path_str = str(feed_path)
                if (
                    'results' in feed_path_str
                    and not feed_path_str.startswith('/')
                ):
                    # Относительный путь - используем текущую директорию
                    results_dir = Path.cwd() / 'results'
                else:
                    results_dir = Path(feed_path_str).parent
        else:
            results_dir = Path.cwd() / 'results'

        # Создаёт папку, если её нет
        results_dir.mkdir(parents=True, exist_ok=True)

        current_dt = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')

        # Сохраняет файл со списком PEP
        pep_filename = results_dir / f'pep_{current_dt}.csv'
        with open(pep_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['number', 'name', 'status'])
            for item in self.pep_items:
                writer.writerow([item['number'], item['name'], item['status']])

        # Сохраняет файл со сводкой по статусам
        summary_filename = results_dir / f'status_summary_{current_dt}.csv'
        result = [('Статус', 'Количество')]
        result.extend(self.status_count.items())
        result.append(('Total', sum(self.status_count.values())))

        with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(result)
