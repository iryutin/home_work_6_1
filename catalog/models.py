from django.db import models

class Category (models.Model):
    name_category = models.CharField(max_length= 150)
    description = models.TextField(null=True)

class Product(models.Model):
    name = models.CharField(max_length= 150, verbose_name= "Имя_продукта")
    description = models.TextField(null=True)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at  = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

