from django import forms

from .models import Category, Product, Version


class AddProductForm(forms.ModelForm):
    BANNED_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ['title', 'description', 'photo', 'category', 'price', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название продукта'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control',
                                                 'placeholder': 'Вводите данные с разделителем ";"', }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'is_published': forms.Select(attrs={'class': 'form-control'}),
        }

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана',
                                      label='Категория',
                                      widget=Meta.widgets['category'],
                                      )

    is_published = forms.TypedChoiceField(choices=Product.Status.choices,
                                          coerce=int,
                                          widget=Meta.widgets['is_published'],
                                          initial=Product.Status.PUBLISHED,
                                          label='Статус',
                                          )

    def check_ban_words(self, attr_name, msg_err):
        attr_name = self.cleaned_data[attr_name]
        attr_name_lower = attr_name.lower()
        for word in self.BANNED_WORDS:
            if word in attr_name_lower:
                raise forms.ValidationError(msg_err.format(word))
        return attr_name

    def clean_title(self):
        return self.check_ban_words('title', 'Запрещено в названии использовать слово: "{}"')

    def clean_description(self):
        return self.check_ban_words('description', 'Запрещено в описании использовать слово: "{}"')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
            'description': forms.Textarea(
                attrs={'cols': 50, 'rows': 5, 'class': 'form-control', 'placeholder': 'Описание категории'}),
        }


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = ['product', 'version_number', 'title', 'is_active']
        widgets = {
            'version_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']

        if is_active:
            checkbox_counter = 0
            for for_, value in self.data.items():
                if for_.endswith('is_active') and value == 'on':
                    if (checkbox_counter := checkbox_counter + 1) > 1:
                        raise forms.ValidationError('Можно выбрать только одну активную версию')

        return is_active
