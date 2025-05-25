from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
from .apps import UserConfig

app_name = UserConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]