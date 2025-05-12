from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

        def clean(self):
            ban_words = ['казино', 'биржа', 'обман', 'криптовалюта', 'дешево', 'полиция', 'крипта', 'бесплатно', 'радар']
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            print(cleaned_data)
            description = cleaned_data.get('description')
            for word in ban_words:
                if word in name.lower() or word in description.lower():
                    self.add_error('name', f'В имени и описании не должно быть запрещённых слов\n{ban_words}')

        def clean_price(self):
            price = self.cleaned_data.get('price')
            if price < 0:
                raise ValidationError(f'Цена не может быть ниже нуля')
            return price

        def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                if image.size > 5 * 1024 * 1024:  # 5MB
                    raise ValidationError('Файл слишком большой')
                if image.content_type not in ['image/jpeg', 'image/png']:
                    raise ValidationError('Неподдерживаемый формат')
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
            'type': 'image'
        })