from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES,
        default='client', verbose_name='Роль'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} ({self.get_role_display()})'



class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL-идентификатор')
    icon = models.CharField(max_length=255, blank=True, verbose_name='Иконка')
    sort_order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'categories'
        ordering = ['sort_order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT,
        related_name='products', verbose_name='Категория'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    brand = models.CharField(max_length=50, blank=True, verbose_name='Бренд')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.CharField(max_length=255, blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    stock = models.IntegerField(default=0, verbose_name='Остаток')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f'{self.name} ({self.brand})'


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='specifications', verbose_name='Товар'
    )
    spec_key = models.CharField(max_length=50, verbose_name='Ключ')
    spec_value = models.CharField(max_length=100, verbose_name='Значение')

    class Meta:
        db_table = 'specifications'
        unique_together = ('product', 'spec_key')
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        indexes = [
            models.Index(fields=['spec_key', 'spec_value']),
        ]

    def __str__(self):
        return f'{self.spec_key}: {self.spec_value}'


class Build(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='builds', verbose_name='Пользователь',
        null=True, blank=True
    )
    name = models.CharField(max_length=100, default='Моя сборка', verbose_name='Название')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Итоговая цена'
    )
    total_tdp = models.IntegerField(default=0, verbose_name='Итоговое TDP')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'builds'
        ordering = ['-created_at']
        verbose_name = 'Сборка'
        verbose_name_plural = 'Сборки'

    def __str__(self):
        email = self.user.email if self.user else 'Гость'
        return f'{self.name} ({email})'

class BuildItem(models.Model):
    build = models.ForeignKey(
        Build, on_delete=models.CASCADE,
        related_name='items', verbose_name='Сборка'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        db_table = 'build_items'
        unique_together = ('build', 'product')
        verbose_name = 'Элемент сборки'
        verbose_name_plural = 'Элементы сборки'

    def __str__(self):
        return f'{self.build.name} -> {self.product.name} x{self.quantity}'



class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('assembling', 'Сборка'),
        ('shipped', 'Отправлен'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.RESTRICT,
        related_name='orders', verbose_name='Пользователь',
        null=True, blank=True
    )
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES,
        default='new', verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Итоговая цена'
    )
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Способ оплаты')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id} ({self.get_status_display()})'

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_at_moment = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа'
    )

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Товар'
    )
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    text = models.TextField(blank=True, verbose_name='Текст отзыва')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ('user', 'product')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.user.email} -> {self.product.name}: {self.rating}★'