from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("create/", views.ProductCreate.as_view(), name="product_create"),
    path("", views.ProductListView.as_view(), name="home"),
    path("product_info/<int:pk>", views.ProductDetailView.as_view(), name="product_info"),
    path("update/<int:pk>", views.ProductUpdateView.as_view(), name="product_update"),
    path("delite/<int:pk>", views.ProductDeliteViev.as_view(), name="product_delite"),
]
