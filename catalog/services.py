from .models import Product, Category

from catalog.models import Product

def get_products_by_category(category_pk):
    """Возвращает все продукты указанной категории"""
    return Product.objects.filter(category__pk=category_pk)