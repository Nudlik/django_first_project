from django import forms
from .models import Category


class AddProductForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Название продукта',
                                                                          }), label='Название')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 50,
                                                               'rows': 5,
                                                               'class': 'form-control',
                                                               'placeholder': 'Вводите данные с разделителем ";"',
                                                               }
                                                        ),
                                  required=False,
                                  label='Описание',
                                  )
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана',
                                      label='Категория',
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      )
    price = forms.DecimalField(max_digits=12,
                               decimal_places=2,
                               min_value=0,
                               label='Стоимость',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
                               )
    is_published = forms.BooleanField(initial=True, label='Опубликовано')
