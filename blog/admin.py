from django.contrib import admin
from .models import Post


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "publication", "views")
    list_filter = ("name",)
    search_fields = ("name", "description")
