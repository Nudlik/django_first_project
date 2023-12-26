from django.db import models
from django.urls import reverse

NULLABLE = {'null': True, 'blank': True}


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.IntegerChoices):
        PUBLISHED = 1, 'Опубликовано'
        DRAFT = 0, 'Черновик'

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/products/%Y/%m/%d/', **NULLABLE, verbose_name='Фото')
    category = models.ForeignKey(to='Category',
                                 on_delete=models.PROTECT,
                                 related_name='products',
                                 verbose_name='Категория'
                                 )
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Цена')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED, verbose_name='Опубликовано')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('catalog:view_product', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('catalog:view_category', kwargs={'pk': self.pk})


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='version', verbose_name='Продукт')
    version_number = models.PositiveIntegerField(verbose_name='Номер версии')
    title = models.CharField(max_length=255, **NULLABLE, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, **NULLABLE, verbose_name='Активна')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ['-is_active', '-version_number']


class Contact(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    inn = models.CharField(max_length=50, unique=True, verbose_name='ИНН')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'({self.pk}){self.inn}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['city']
