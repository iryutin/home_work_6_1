from django import forms
from .models import Product
from django.core.exceptions import ValidationError
import os

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean(self):
        ban_words = ['казино', 'биржа', 'обман', 'криптовалюта', 'дешево', 'полиция', 'крипта', 'бесплатно', 'радар']
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        if name and description:
            for word in ban_words:
                if word in name.lower() or word in description.lower():
                    raise ValidationError({
    'name': f'Содержит запрещенное слово. Нельзя использовать: {ban_words}',
    'description': 'Проверьте описание на запрещенные слова'
})

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError(f'Цена не может быть ниже нуля')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Проверка размера
        if image.size > 5 * 1024 * 1024:
            raise ValidationError('Файл слишком большой (максимум 5 МБ)')

        # Проверка расширения файла
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError('Неподдерживаемый формат (разрешены только JPEG/PNG)')

        return image

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите наименование продукта'  # Текст подсказки внутри поля
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание продукта'
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену продукта'
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
        })