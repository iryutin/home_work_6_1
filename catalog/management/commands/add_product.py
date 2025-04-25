from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add test students to the database"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name_category="Категория 1")

        product = [
            {
                "name": "samsung",
                "description": "Что то",
                "category": category,
                "price": 123,
                "image": "/test_ima.png",
                'created_at': '2025-04-25'
            },
            {
                "name": "ifon",
                "description": "Что то",
                "category": category,
                "price": 321,
                "image": "/test_ima.png",
                'created_at': '2025-04-25'
            },
            {
                "name": "pirat",
                "description": "Что то",
                "category": category,
                "price": 231,
                "image": "/test_ima.png",
                'created_at': '2025-04-25'
            },
        ]

        for student_data in product:
            product, created = Product.objects.get_or_create(**student_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added product: {product.name} {product.price}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Product already exists: {product.name} {product.price}"
                    )
                )
