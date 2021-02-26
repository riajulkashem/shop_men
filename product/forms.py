from django import forms
from django.forms import Textarea

from product.models import Brand, Category, Product


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']

        widgets = {
            'description': Textarea(attrs={'rows': 1, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BrandForm, self).__init__(*args, **kwargs)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'unit', 'description']

        widgets = {
            'description': Textarea(attrs={'rows': 1, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'brand', 'category',
            'photo', 'purchase_price',
            'sell_price', 'alert_quantity', 'description',
            'stock'
        ]

        widgets = {
            'description': Textarea(attrs={'rows': 1, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProductForm, self).__init__(*args, **kwargs)
