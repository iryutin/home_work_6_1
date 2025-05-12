from django.urls import path, include
from . import views
from .apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("post_list/create/", views.PostCreate.as_view(), name="post_create"),
    path("post_list/list/", views.PostListView.as_view(), name="post_list"),
    path("post_list/detail/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("post_list/update/<int:pk>", views.PostUpdateView.as_view(), name="post_update"),
    path("post_list/delite/<int:pk>", views.PostDeliteViev.as_view(), name="post_delite"),

]
