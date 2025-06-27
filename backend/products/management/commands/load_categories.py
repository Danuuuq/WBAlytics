from django.core.management.base import BaseCommand
from products.utils.category_loader import parse_wb_categories


class Command(BaseCommand):
    help = 'Загружает категории с WB'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаем загрузку категорий')
        try:
            parse_wb_categories()
            self.stdout.write(
                self.style.SUCCESS('✅ Категории успешно загружены'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка при загрузке категорий: {e}'))
            raise
