from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.db import models
from datetime import datetime


class Device(models.Model):
    """Оборудование"""

    class Meta:
        db_table = "devices"
        verbose_name = "Доступное оборудование"
        verbose_name_plural = "Доступное оборудование"

    manufacturer = models.TextField(verbose_name="Производитель")
    model = models.TextField(verbose_name="Модель")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class Customer(models.Model):
    """Пользователи оборудования"""

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагента"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.CharField(max_length=64, verbose_name="Адрес организации")
    customer_city = models.TextField(verbose_name="Город организации")

    def __str__(self):
        return f"{self.customer_name} по адресу {self.customer_address}"


class DeviceInFields(models.Model):
    """Оборудование в полях"""

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"

    serial_number = models.CharField(max_length=64, verbose_name="Номер серии")
    owner_status = models.TextField(verbose_name="Статус принадлежности")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Айди оборудования")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Пользователь")

    def __str__(self):
        return f"{self.analyzer} с/н {self.serial_number} в {self.customer}"


class Order(models.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "нужна информация"))

    device = models.ForeignKey(DeviceInFields, on_delete=models.RESTRICT, verbose_name="Оборудование")
    # customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Пользователь конечный")
    order_description = models.TextField(verbose_name="Описание завявки")
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    last_updated_dt = models.DateTimeField(blank=True, null=True, verbose_name="Время изменения статуса")
    order_status = models.TextField(verbose_name="Статус заявки", choices=statuses)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)


