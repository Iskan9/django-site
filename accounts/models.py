
from django.db import models

from django.db import models

# Create your models here.


class Customer(models.Model):
    """Клиенты"""
    name = models.CharField(max_length=200, null=True, verbose_name="имя")
    phone = models.CharField(max_length=200, null=True, verbose_name="телефон")
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")

    def __str__(self):
        return self.name

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Клиент"  # имя для объекта в единственном числе
        verbose_name_plural = "Клиенты"  # имя для объекта во множественном числе


class Product(models.Model):
    CATEGORY = (
            ('В помещении', 'В помещении'),  # 'Indoor', 'Indoor'
            ('На улице', 'На улице'),  # 'Out Door', 'Out Door'
            )

    name = models.CharField(max_length=200, null=True, verbose_name="имя")
    price = models.FloatField(null=True, verbose_name="цена")
    category = models.CharField(max_length=200, null=True, choices=CATEGORY, verbose_name="категория")
    description = models.CharField(max_length=200, null=True, verbose_name="описание")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Продукт"  # имя для объекта в единственном числе
        verbose_name_plural = "Продукты"  # имя для объекта во множественном числе


class Order(models.Model):
    STATUS = (
            ('В ожидании', 'В ожидании'),  # 'Pending', 'Pending'
            ('В пути', 'В пути'),  # 'Out for delivery', 'Out for delivery'
            ('Доставлено', 'Доставлено'),  # 'Delivered', 'Delivered'
            )

    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")
    status = models.CharField(max_length=200, null=True, choices=STATUS, verbose_name="статус")

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Заказ"  # имя для объекта в единственном числе
        verbose_name_plural = "Заказы"  # имя для объекта во множественном числе
