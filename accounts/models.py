

from django.db import models

from django.contrib.auth.models import User  # импорируем User для установления соотношения 1 к 1 для пользователя
#  и клиента


class Customer(models.Model):
    """Клиенты"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="пользователь")
    # пользователь соответсвует клиенту
    name = models.CharField(max_length=200, null=True, verbose_name="имя")
    phone = models.CharField(max_length=200, null=True, verbose_name="телефон")
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True, verbose_name="фото профиля")
    # для ImageField нужен pillow, установим его через pip
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")

    def __str__(self):
        return self.name

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Клиент"  # имя для объекта в единственном числе
        verbose_name_plural = "Клиенты"  # имя для объекта во множественном числе


class Tag(models.Model):
    """Клиенты"""
    name = models.CharField(max_length=200, null=True, verbose_name="имя")

    def __str__(self):
        return self.name

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Тег"  # имя для объекта в единственном числе
        verbose_name_plural = "Теги"  # имя для объекта во множественном числе


class Product(models.Model):
    """Товар"""
    CATEGORY = (
            ('В помещении', 'В помещении'),  # 'Indoor', 'Indoor'
            ('На улице', 'На улице'),  # 'Out Door', 'Out Door'
            )

    name = models.CharField(max_length=200, null=True, verbose_name="имя")
    price = models.FloatField(null=True, verbose_name="цена")
    category = models.CharField(max_length=200, null=True, choices=CATEGORY, verbose_name="категория")
    description = models.CharField(max_length=200, null=True, verbose_name="описание", blank=True)
    # blank=True, означает поле не обязательное для заполнения
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")
    tags = models.ManyToManyField(Tag, verbose_name="теги")

    def __str__(self):
        return self.name

    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Продукт"  # имя для объекта в единственном числе
        verbose_name_plural = "Продукты"  # имя для объекта во множественном числе




class Order(models.Model):
    """Заказ"""
    STATUS = (
            ('В ожидании', 'В ожидании'),  # 'Pending', 'Pending'
            ('В пути', 'В пути'),  # 'Out for delivery', 'Out for delivery'
            ('Доставлено', 'Доставлено'),  # 'Delivered', 'Delivered'
            )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, verbose_name="клиент")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="продукт")

    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="дата создания")
    status = models.CharField(max_length=200, null=True, choices=STATUS, verbose_name="статус")
    note = models.CharField(max_length=200, null=True, verbose_name="запись")

    def __str__(self):
        return self.product.name


    class Meta:  # контейнер класса с некоторыми опциями: метаданные
        verbose_name = "Заказ"  # имя для объекта в единственном числе
        verbose_name_plural = "Заказы"  # имя для объекта во множественном числе
