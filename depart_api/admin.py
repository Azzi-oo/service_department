from django.contrib import admin

from .models import Order, Device, Customer, DeviceInFields


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer', 'model')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_address', 'customer_city')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'customer', 'order_description', 'created_dt', 'last_updated_dt', 'order_status')


class DeviceInFieldsAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'owner_status', 'analyzer_id', 'customer_id')


admin.site.register(Order, OrderAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeviceInFields, DeviceInFieldsAdmin)
