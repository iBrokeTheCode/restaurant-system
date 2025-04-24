from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint


class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Menu Categories'

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name='items')
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(price__gte=0),
                            name='menu_item_price_gte_0)',
                            violation_error_message='Price must be greater than or equal to 0'),
        ]

    def __str__(self) -> str:
        return self.name
