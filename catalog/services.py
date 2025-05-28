from .models import Product, Category

from catalog.models import Product

def get_products_by_category(category):
    """Возвращает все продукты указанной категории"""
    return Product.objects.filter(
        category__slug=category,
        status='published'  # Только опубликованные продукты
    ).select_related('category', 'owner').order_by('-created_at')