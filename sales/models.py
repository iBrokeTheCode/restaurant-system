from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

from orders.models import Order


class Sale(models.Model):
    class PaymentMethodChoice(models.TextChoices):
        CASH = ('cash', 'Cash')
        BANK_APP = ('bank app', 'Bank App')

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='sale')
    payment_method = models.CharField(
        max_length=10, choices=PaymentMethodChoice, default=PaymentMethodChoice.CASH
    )
    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(amount__gte=0.00),
                name='sale_amount_gte_0',
                violation_error_message='Amount must be greater than or equal to 0',
            ),
        ]
        ordering = ('-payment_time',)

    def save(self, *args, **kwargs):
        if self.order and self.amount is None:
            self.amount = self.order.total
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Sale #{self.pk} - Order #{self.order.pk} - {self.get_payment_method_display()}'  # type: ignore
