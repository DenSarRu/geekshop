from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
        unique=True
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name='имя продукта',
        max_length=128)

    image = models.ImageField(
        upload_to='products_images',
        blank=True
    )

    short_desc = models.CharField(
        verbose_name='краткое описание продукта',
        max_length=60,
        blank=True
    )

    description = models.TextField(
        verbose_name='описание продукта',
        blank=True
    )

    price = models.DecimalField(
        verbose_name='цена продукта',
        max_digits=8,
        decimal_places=2,
        default=0
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество на складе',
        default=0)

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        ordering = ['created']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Contacts(models.Model):
    city = models.CharField(
        verbose_name='город',
        max_length=64
    )

    phone = models.CharField(
        verbose_name='номер телефона',
        max_length=32
    )

    email = models.EmailField(
        verbose_name='e-mail'
    )

    address = models.TextField(
        verbose_name='Почтовый адрес'
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.city}"

    class Meta:
        ordering = ['city']
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
