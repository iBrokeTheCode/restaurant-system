from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q


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
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name='items'
    )
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        constraints = [
            CheckConstraint(
                check=Q(price__gte=0),
                name='menu_item_price_gte_0)',
                violation_error_message='Price must be greater than or equal to 0',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class DailyMenu(models.Model):
    date = models.DateField(unique=True)
    menu_items = models.ManyToManyField(MenuItem, related_name='daily_menus')

    class Meta:
        verbose_name = 'Daily Menu'
        verbose_name_plural = 'Daily Menus'
        ordering = ('-date',)

    def __str__(self) -> str:
        return f'Menu for {self.date}'
