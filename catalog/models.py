from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name_category = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


    def __str__(self):
        return self.name_category


class Product(models.Model):
    PUBLICATION_STATUS = [
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
        ('archived', 'В архиве'),
    ]
    status = models.CharField(
        max_length=20,
        choices=PUBLICATION_STATUS,
        default='draft',
        verbose_name='Статус публикации'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='products',
        blank=True, null=True
    )
    name = models.CharField(max_length=150, verbose_name="Имя_продукта")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["description", "price"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ('can_delete_any_product', 'Может удалять ЛЮБОЙ продукт'),
        ]

    def __str__(self):
        return self.name
