from django.contrib import admin
from . import models as sample_models


@admin.register(sample_models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


@admin.register(sample_models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(sample_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete')


@admin.register(sample_models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
