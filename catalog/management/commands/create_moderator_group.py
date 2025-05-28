from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Creates Moderator group with permissions'

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Добавляем права
        permissions = [
            'can_unpublish_product',
            'delete_product',
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(
                    codename=perm,
                    content_type=content_type
                )
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm} not found'))

        self.stdout.write(self.style.SUCCESS('Группа модераторов успешно создана'))