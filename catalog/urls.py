from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("create/", views.ProductCreate.as_view(), name="product_create"),
    path("", views.ProductListView.as_view(), name="home"),
    path("product_info/<int:pk>", views.ProductDetailView.as_view(), name="product_info"),
    path("update/<int:pk>", views.ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete/', views.ProductDeliteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', views.ProductUnpublishView.as_view(), name='product_unpublish'),
    path('product/category/<int:pk>', views.ProductsByCategoryDetailView.as_view(), name='products_by_category'),
    path('product/category/', views.CategoryListView.as_view(), name='category_list'),
]
