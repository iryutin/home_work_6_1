from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
     email = models.EmailField(unique=True)
     phone_namber = models.CharField(max_length=15, blank=True, null=True)
     avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
     country = models.CharField(
          max_length=100,
          blank=True,
          null=True
     )

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['username']

     # Меняем поле для авторизации на email
     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['username']  # username требуется для createsuperuser

     class Meta:
          verbose_name = 'user'
          verbose_name_plural = 'users'

     def __str__(self):
         return  self.email
