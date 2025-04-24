from django.db import models

from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint

from decimal import Decimal

from tables.models import Table
from menu.models import MenuItem


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        PENDING = ('pending', 'Pending')
        IN_PROGRESS = ('in progress', 'In Progress')
        SERVED = ('served', 'Served')
        PAID = ('paid', 'Paid')
        CANCELLED = ('cancelled', 'Cancelled')

    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15, choices=OrderStatusChoices, default=OrderStatusChoices.PENDING)

    @property
    def total(self):
        return sum(
            item.total_price for item in self.items.all()  # type: ignore
            if item.total_price is not None
        ) or Decimal('0.00')

    def __str__(self) -> str:
        return f'Order #{self.pk} - Table {self.table.table_number if self.table else "N/A"}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, validators=[
                                     MinValueValidator(0.00)])
    note = models.TextField(blank=True, default='')

    @property
    def total_price(self):
        if self.quantity is not None and self.unit_price is not None:
            return self.quantity * self.unit_price
        return Decimal(0.00)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(quantity__gte=1),
                            name='order_item_quantity_gte_1',
                            violation_error_message='Quantity must be greater than or equal to 1'),
            CheckConstraint(check=Q(unit_price__gte=0),
                            name='order_item_price_gte_0',
                            violation_error_message='Price must be greater than or equal to 0'),
        ]

    def save(self, *args, **kwargs):
        if self.unit_price is None and self.menu_item:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.quantity} x {self.menu_item.name}'
