import csv
from datetime import datetime, timezone
from pathlib import Path

from .settings import BASE_DIR


class PepParsePipeline:
    """Pipeline сохранения статистики по документам PEP."""

    def open_spider(self, spider):
        """Инициализация словаря и списка при запуске паука."""
        self.status_count = {}
        self.pep_items = []

        # Очищаем папку результатов перед запуском
        feeds = spider.crawler.settings.getdict('FEEDS') or {}
        if feeds:
            feed_path = list(feeds.keys())[0]
            if isinstance(feed_path, Path):
                results_dir = feed_path.parent
            else:
                feed_path_str = str(feed_path)
                if 'tests' in feed_path_str and '_tmp' in feed_path_str:
                    results_dir = Path(feed_path_str).parent
                else:
                    results_dir = BASE_DIR / 'results'
        else:
            results_dir = BASE_DIR / 'results'

        # Очищаем папку от старых файлов
        if results_dir.exists():
            for file in results_dir.glob('*.csv'):
                file.unlink()
                spider.logger.info(f'Удалён старый файл: {file.name}')

    def process_item(self, item, spider):
        """Подсчет количества статусов и сохранение PEP."""
        status = item.get('status')
        self.status_count[status] = (self.status_count.get(status, 0) + 1)
        self.pep_items.append(item)
        return item

    def close_spider(self, spider):
        """Запись значений в файлы."""
        # Получаем настройки FEEDS из паука
        feeds = spider.crawler.settings.getdict('FEEDS') or {}

        # Определяем директорию для сохранения
        if feeds:
            feed_path = list(feeds.keys())[0]

            if isinstance(feed_path, Path):
                results_dir = feed_path.parent
            else:
                feed_path_str = str(feed_path)
                if 'tests' in feed_path_str and '_tmp' in feed_path_str:
                    results_dir = Path(feed_path_str).parent
                else:
                    results_dir = BASE_DIR / 'results'
        else:
            results_dir = BASE_DIR / 'results'

        # Создаём папку
        results_dir.mkdir(parents=True, exist_ok=True)

        current_dt = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')

        # 1. Сохраняем файл PEP
        pep_filename = results_dir / f'pep_{current_dt}.csv'
        with open(pep_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['number', 'name', 'status'])
            for item in self.pep_items:
                writer.writerow([item['number'], item['name'], item['status']])

        # 2. Сохраняем сводку
        summary_filename = results_dir / f'status_summary_{current_dt}.csv'
        result = [('Статус', 'Количество')]
        result.extend(self.status_count.items())
        result.append(('Total', sum(self.status_count.values())))

        with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(result)
