import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.db import transaction

from products.models import Product, Category
from product_analytics.constants import SettingsParse


def parse_wb_by_category(
    category_name: str,
    min_price: int | None = None,
    max_price: int | None = None,
    max_workers: int = 5
):
    """Многопоточный парсинг."""
    category = Category.objects.filter(name=category_name).first()
    if not category:
        return
    shard = category.shard
    query = category.query
    if not shard or not query:
        return
    priceU = ''
    if min_price or max_price:
        priceU = f'&priceU={min_price or 0}00;{max_price or 99999999999}00'
    def fetch_page_sync(page):
        url = (f'https://catalog.wb.ru/catalog/{shard}/v2/catalog'
               f'?ab_testing=false&appType=1&{query}'
               '&curr=rub&dest=-1257786&'
               f'hide_dtype=13&lang=ru&page={page}'
               '&sort=popular&spp=30') + priceU
        try:
            response = requests.get(url, headers=SettingsParse.HEADERS, timeout=30)
            if not response.ok:
                return page, []
            data = response.json()
            items = data.get('data', {}).get('products', [])
            print(f'Загружена страница {page}, товаров: {len(items)}')
            return page, items
        except Exception as e:
            print(f'Ошибка при загрузке страницы {page}: {e}')
            return page, []
    all_products_data = []
    page = 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            future_to_page = {
                executor.submit(fetch_page_sync, p): p 
                for p in range(page, page + max_workers)
            }
            empty_pages = 0
            for future in as_completed(future_to_page):
                page_num, items = future.result()
                if not items:
                    empty_pages += 1
                else:
                    all_products_data.extend(items)
            if empty_pages == len(future_to_page):
                break
            page += max_workers
    return save_products_batch_sync(all_products_data, category)


def save_products_batch_sync(products_data, category):
    """Синхронная версия batch-сохранения"""
    print(f'Начинаем сохранение {len(products_data)} товаров...')
    products_to_process = []
    for item in products_data:
        try:
            prices = item.get('sizes', [{}])[0].get('price', {})
            name = item.get('name', 'Без названия')
            price = prices.get('basic', 0) / 100
            discounted_price = prices.get('product', 0) / 100
            rating = item.get('reviewRating', 0)
            reviews = item.get('feedbacks', 0)
            products_to_process.append({
                'name': name,
                'price': price,
                'discounted_price': discounted_price,
                'rating': rating,
                'review_count': reviews,
            })
        except Exception as e:
            continue
    if not products_to_process:
        return []
    # Batch операции с БД
    with transaction.atomic():
        existing_names = [p['name'] for p in products_to_process]
        existing_products = {
            p.name: p for p in Product.objects.filter(
                name__in=existing_names,
                category=category
            ).select_for_update()
        }
        products_to_create = []
        products_to_update = []
        result_products = []
        
        for product_data in products_to_process:
            name = product_data['name']
            
            if name in existing_products:
                product = existing_products[name]
                product.price = product_data['price']
                product.discounted_price = product_data['discounted_price']
                product.rating = product_data['rating']
                product.review_count = product_data['review_count']
                products_to_update.append(product)
                result_products.append(product)
            else:
                product = Product(
                    name=name,
                    category=category,
                    price=product_data['price'],
                    discounted_price=product_data['discounted_price'],
                    rating=product_data['rating'],
                    review_count=product_data['review_count'],
                )
                products_to_create.append(product)
                result_products.append(product)
        if products_to_create:
            Product.objects.bulk_create(products_to_create, batch_size=5000)
        
        if products_to_update:
            Product.objects.bulk_update(
                products_to_update,
                ['price', 'discounted_price', 'rating', 'review_count'],
                batch_size=5000
            )
    return result_products
