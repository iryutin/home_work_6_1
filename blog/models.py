from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_поста")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='post')
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    publication = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["description", "views"]

    def __str__(self):
        return self.name
