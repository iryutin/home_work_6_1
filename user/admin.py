from django.contrib import admin
from .models import UserModel


@admin.register(UserModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_namber", "country")
    list_filter = ("email",)
    search_fields = ("email", "country")