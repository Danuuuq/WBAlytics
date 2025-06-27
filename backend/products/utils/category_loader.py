import requests
from products.models import Category
from django.db import transaction
from typing import Any

from product_analytics.constants import SettingsParse


def parse_wb_categories():
    """Парсинг категорий для загрузки и обновлений в будущем."""
    try:
        response = requests.get(SettingsParse.URL_CATEGORY_WB, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f'Ошибка сетевого запроса: {e}')
        return
    except ValueError as e:
        print(f'Ошибка парсинга JSON: {e}')
        return
    categories_data = []
    def collect_categories(nodes: list[dict[Any, Any]], depth: int = 0):
        """Сбор категорий с ограничением глубины рекурсии"""
        if depth > 10:
            return
        if not isinstance(nodes, list):
            return
        for node in nodes:
            if not isinstance(node, dict):
                continue
            seo_name = node.get('seo')
            if seo_name and isinstance(seo_name, str) and seo_name.strip():
                shard = node.get('shard', '')
                query = node.get('query', '')
                if isinstance(shard, str) and isinstance(query, str):
                    categories_data.append({
                        'name': seo_name.strip(),
                        'shard': shard.strip(),
                        'query': query.strip()
                    })
            childs = node.get('childs')
            if childs:
                collect_categories(childs, depth + 1)
    collect_categories(data)
    if not categories_data:
        print('Не найдено валидных категорий')
        return
    unique_categories = {}
    for cat in categories_data:
        unique_categories[cat['name']] = cat

    categories_data = list(unique_categories.values())
    print(f'Найдено {len(categories_data)} уникальных категорий')
    try:
        with transaction.atomic():
            existing_names = [cat['name'] for cat in categories_data]
            existing_categories = set(
                Category.objects.filter(name__in=existing_names).values_list('name', flat=True)
            )
            categories_to_create = [
                Category(
                    name=cat_data['name'],
                    shard=cat_data['shard'],
                    query=cat_data['query']
                )
                for cat_data in categories_data
                if cat_data['name'] not in existing_categories
            ]
            if categories_to_create:
                Category.objects.bulk_create(categories_to_create, batch_size=500)
                print(f'Успешно создано {len(categories_to_create)} категорий')
            else:
                print('Все категории уже существуют в базе')
    except Exception as e:
        print(f'Ошибка при сохранении в базу данных: {e}')
        return

    total_categories = Category.objects.count()
    print(f'Загрузка завершена. Всего категорий в базе: {total_categories}')
