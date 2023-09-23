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
        verbose_name = "Пользователь оборудования"
        verbose_name_plural = "Пользователи оборудования"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.CharField(max_length=64, verbose_name="Адрес организации")
    customer_city = models.TextField(verbose_name="Город организации")

    def __str__(self):
        return self.customer_name


class DeviceInFields(models.Model):
    """Оборудование в полях"""

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"

    serial_number = models.CharField(max_length=64, verbose_name="Номер серии")
    owner_status = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Статус пользователя")
    analyzer_id = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Айди оборудования")
    customer_id = models.TextField(verbose_name="Статус принаджежности")

    def __str__(self):
        return f"{self.serial_number} {self.analyzer_id}"


def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order_status)s is wrong order status'),
            params={'order_status': order_status},
        )


class Order(models.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    device = models.ForeignKey(DeviceInFields, on_delete=models.RESTRICT, verbose_name="Оборудование")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Пользователь конечный")
    order_description = models.TextField(verbose_name="Описание завявки")
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    last_updated_dt = models.DateTimeField(blank=True, null=True, verbose_name="Время изменения статуса")
    order_status = models.TextField(verbose_name="Статус заявки", validators=[status_validator])

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)


