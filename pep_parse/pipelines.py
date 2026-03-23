import csv
from datetime import datetime

from itemadapter import ItemAdapter


class PepParsePipeline:
    """Pipeline для подсчета статусов PEP и сохранения сводки."""

    def __init__(self):
        """Счетчик статусов."""
        self.status_counts = {}

    def open_spider(self, spider):
        """Вызывается при открытии паука."""
        spider.logger.info('Pipeline открыт. Начинаем подсчет статусов.')

    def process_item(self, item, spider):
        """Обрабатывает каждый Item, подсчитывая статусы."""
        adapter = ItemAdapter(item)
        status = adapter.get('status')

        if status:
            self.status_counts[status] = self.status_counts.get(status, 0) + 1

        return item

    def close_spider(self, spider):
        """При закрытии паука формирует CSV-файл со сводкой по статусам."""
        # Формирует имя файла с текущей датой и временем
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'results/status_summary_{timestamp}.csv'

        # Сортирует статусы по алфавиту
        sorted_statuses = sorted(self.status_counts.items())

        # Подсчитывает общее количество
        total = sum(self.status_counts.values())

        # Записывает данные в CSV
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])

            for status, count in sorted_statuses:
                writer.writerow([status, count])

            writer.writerow(['Total', total])

        spider.logger.info(f'Сводка по статусам сохранена в {filename}')
