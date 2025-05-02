from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name_category


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_продукта")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["description", "price"]

    def __str__(self):
        return self.name
