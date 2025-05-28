from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_category")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'owner', 'created_at')
    list_filter = ('status', 'category', 'owner')
    search_fields = ('name', 'description', 'owner__username')

    def save_model(self, request, obj, form, change):
        if not change:  # Если это создание нового объекта
            obj.owner = request.user
        super().save_model(request, obj, form, change)
