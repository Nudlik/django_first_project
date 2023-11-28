from django import forms
from .models import Category, Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'photo', 'category', 'price', 'is_published']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Название продукта'
                }),
            'description': forms.Textarea(
                attrs={
                    'cols': 50,
                    'rows': 5,
                    'class': 'form-control',
                    'placeholder': 'Вводите данные с разделителем ";"',
                }),
            'photo': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00'
                }),
            'is_published': forms.Select(
                attrs={
                    'class': 'form-control'
                })
        }

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана',
                                      label='Категория',
                                      widget=Meta.widgets['category'],
                                      )

    photo = forms.ImageField(required=False,
                             widget=Meta.widgets['photo'],
                             )
    is_published = forms.TypedChoiceField(choices=Product.Status.choices,
                                          coerce=int,
                                          widget=Meta.widgets['is_published'],
                                          initial=Product.Status.PUBLISHED,
                                          label='Статус',
                                          )
