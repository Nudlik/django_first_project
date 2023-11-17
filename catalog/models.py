from django.db import models

NULLABLE = {'null': True, 'blank': True}


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', **NULLABLE, verbose_name='Фото')
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
        return f'({self.pk}){self.title}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-time_create']


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'({self.pk}){self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Contact(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    inn = models.CharField(max_length=50, unique=True, verbose_name='ИНН')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'({self.inn}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['city']
