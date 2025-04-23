from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint

from orders.models import Order


class Sale(models.Model):
    class PaymentMethodChoice(models.TextChoices):
        CASH = ('cash', 'Cash')
        BANK_APP = ('bank app', 'Bank App')

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='sale')
    payment_method = models.CharField(
        max_length=10, choices=PaymentMethodChoice, default=PaymentMethodChoice.CASH)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[
                                 MinValueValidator(0.01)])
    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(amount__gt=0), name='sale_amount_gt_0')
        ]

    def __str__(self) -> str:
        return f'Sale #{self.pk} - Order #{self.order.pk} - {self.payment_method}'
