from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_info

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("product_info/<int:pk>/", product_info, name = "product_info"),
]
