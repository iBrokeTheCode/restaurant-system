from django.db import models

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
        )

    def __str__(self) -> str:
        return f'Order #{self.pk} - Table {self.table.table_number if self.table else "N/A"}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.TextField(blank=True, default='')

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self) -> str:
        return f'{self.quantity} x {self.menu_item.name}'
