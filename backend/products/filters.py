def apply_product_filters(qs, params):
    min_price = params.get('min_price')
    if min_price:
        qs = qs.filter(price__gte=min_price)
    max_price = params.get('max_price')
    if max_price:
        qs = qs.filter(price__lte=max_price)
    min_rating = params.get('min_rating')
    if min_rating:
        qs = qs.filter(rating__gte=min_rating)
    min_reviews = params.get('min_reviews')
    if min_reviews:
        qs = qs.filter(review_count__gte=min_reviews)
    return qs


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def get_value(item, field):
    return getattr(item, field, None) if hasattr(item, field) else item.get(field)

def filter_products(products, params):
    if not products:
        return products
    min_price = safe_float(params.get('min_price'))
    max_price = safe_float(params.get('max_price'))
    min_rating = safe_float(params.get('min_rating'))
    max_rating = safe_float(params.get('max_rating'))
    min_reviews = safe_float(params.get('min_reviews'))
    max_reviews = safe_float(params.get('max_reviews'))
    def passes_filter(product):
        price = safe_float(get_value(product, 'price'))
        rating = safe_float(get_value(product, 'rating'))
        reviews = safe_float(get_value(product, 'review_count'))
        return (
            (not min_price or (price and price >= min_price)) and
            (not max_price or (price and price <= max_price)) and
            (not min_rating or (rating and rating >= min_rating)) and
            (not max_rating or (rating and rating <= max_rating)) and
            (not min_reviews or (reviews and reviews >= min_reviews)) and
            (not max_reviews or (reviews and reviews <= max_reviews))
        )
    
    return [p for p in products if passes_filter(p)]

def sort_products(products_data, sort_by, sort_dir='asc'):
    """Сортировка продуктов с приведением типов (для JSON/Redis)"""
    if not sort_by or not products_data:
        return products_data
    reverse = sort_dir == 'desc'
    numeric_fields = {'price', 'discounted_price', 'rating', 'review_count'}
    def safe_key(p):
        value = p.get(sort_by)
        if value is None:
            return float('-inf') if reverse else float('inf')
        if sort_by in numeric_fields:
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        return str(value)
    try:
        products_data.sort(key=safe_key, reverse=reverse)
    except Exception as e:
        print(f'Ошибка сортировки: {e}')
    return products_data