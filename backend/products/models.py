from django.db import models

from product_analytics.constants import SettingsModels


class Category(models.Model):
    name = models.CharField(
        max_length=SettingsModels.MAX_LENGTH_CATEGORY_FIELD,
        unique=True,
        verbose_name='Имя категории',
    )
    shard = models.CharField(
        max_length=SettingsModels.MAX_LENGTH_CATEGORY_FIELD,
        blank=True,
        null=True,
        verbose_name='Идентификатор WB',
    )
    query = models.CharField(
        max_length=SettingsModels.MAX_LENGTH_CATEGORY_FIELD,
        blank=True,
        null=True,
        verbose_name='Идентификатор коллекции WB',
    )

    class Meta:
        ordering = ('name', 'query')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    name = models.CharField(
        max_length=SettingsModels.MAX_LENGTH_NAME,
        verbose_name='Название товара',
    )
    price = models.DecimalField(
        max_digits=SettingsModels.MAX_DIGITS_PRICE,
        decimal_places=SettingsModels.MAX_DECIMAL_PRICE,
        verbose_name='Цена',
    )
    discounted_price = models.DecimalField(
        max_digits=SettingsModels.MAX_DIGITS_PRICE,
        decimal_places=SettingsModels.MAX_DECIMAL_PRICE,
        verbose_name='Цена со скидкой',
    )
    rating = models.FloatField(verbose_name='Рейтинг')
    review_count = models.IntegerField(verbose_name='Количество отзывов')

    class Meta:
        ordering = ('rating', 'review_count', 'name')
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'products'

    def __str__(self):
        return self.name

    @property
    def discount_amount(self):
        return float(self.price - self.discounted_price)
