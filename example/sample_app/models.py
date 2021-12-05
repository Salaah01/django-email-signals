import typing as _t
from django.db import models
from email_signals.models import EmailSignalMixin


class Customer(models.Model, EmailSignalMixin):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def customer_email(self) -> _t.List[str]:
        return [self.email]


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model, EmailSignalMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def emails(self):
        return [self.customer.email]

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
