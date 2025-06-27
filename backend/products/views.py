from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import filter_products, sort_products
from .utils.wb_scraper import parse_wb_by_category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для отображения доступных категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для отображения актуальных товаров WB.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        """Список продуктов с фильтрацией"""
        category_name = request.GET.get('query')
        if not category_name:
            return Response([])
        cache_key = f'products:{category_name}'
        products_data = cache.get(cache_key)
        sort_by = request.GET.get('sort_by') 
        sort_dir = request.GET.get('sort_dir', 'asc')
        if products_data is None:
            products = parse_wb_by_category(category_name)
            filtered_products = filter_products(products, request.GET)
            serializer = ProductSerializer(filtered_products, many=True)
            filtered_data = serializer.data
            all_serializer = ProductSerializer(products, many=True)
            cache.set(cache_key, all_serializer.data, timeout=60*60)
            filtered_data = sort_products(filtered_data, sort_by, sort_dir)
            return Response(filtered_data)
        else:
            filtered_data = filter_products(products_data, request.GET)
            filtered_data = sort_products(filtered_data, sort_by, sort_dir)
            return Response(filtered_data)
