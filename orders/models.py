from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

from menu.models import DailyMenuItem
from tables.models import Table


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        PENDING = ('pending', 'Pending')
        IN_PROGRESS = ('in progress', 'In Progress')
        SERVED = ('served', 'Served')
        PAID = ('paid', 'Paid')
        CANCELLED = ('cancelled', 'Cancelled')

    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15, choices=OrderStatusChoices, default=OrderStatusChoices.PENDING
    )

    @property
    def total(self):
        return sum(
            item.total_price
            for item in self.items.all()  # type: ignore
            if item.total_price is not None
        ) or Decimal('0.00')

    class Meta:
        ordering = ('-created_at', '-updated_at')

    def __str__(self) -> str:
        return f'#{self.pk} - Table {self.table.table_number if self.table else "N/A"} - Total: S/.{self.total} - {self.get_status_display()}'  # type: ignore


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    daily_menu_item = models.ForeignKey(
        DailyMenuItem, on_delete=models.CASCADE, related_name='order_items'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    note = models.TextField(blank=True, default='')

    @property
    def total_price(self):
        if self.quantity is not None and self.unit_price is not None:
            return self.quantity * self.unit_price
        return Decimal(0.00)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(quantity__gte=1),
                name='order_item_quantity_gte_1',
                violation_error_message='Quantity must be greater than or equal to 1',
            ),
            CheckConstraint(
                check=Q(unit_price__gte=0),
                name='order_item_price_gte_0',
                violation_error_message='Price must be greater than or equal to 0',
            ),
        ]

    def save(self, *args, **kwargs):
        if self.unit_price is None and self.daily_menu_item:
            self.unit_price = self.daily_menu_item.menu_item.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.quantity} x {self.daily_menu_item.menu_item.name}'
