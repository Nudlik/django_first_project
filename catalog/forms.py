from django import forms
from .models import Category


class AddProductForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название')
    description = forms.CharField(widget=forms.Textarea,
                                  required=False,
                                  label='Описание',
                                  help_text='Вводите данные с разделителем ";"')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    price = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label='Стоимость')
    is_published = forms.BooleanField(label='Опубликовано')
