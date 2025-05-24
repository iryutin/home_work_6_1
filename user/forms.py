from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserModel

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'avatar', 'phone_namber', 'country')