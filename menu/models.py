from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint


class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Menu Categories'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name='items'
    )
    image = models.ImageField(upload_to='menu/', blank=True, null=True)

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        constraints = [
            CheckConstraint(
                check=Q(price__gte=0),
                name='menu_item_price_gte_0',
                violation_error_message='Price must be greater than or equal to 0',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class DailyMenu(models.Model):
    date = models.DateField(unique=True)
    menu_items = models.ManyToManyField(
        MenuItem, through='DailyMenuItem', related_name='daily_menus'
    )

    class Meta:
        verbose_name = 'Daily Menu'
        verbose_name_plural = 'Daily Menus'
        ordering = ('-date',)

    def __str__(self) -> str:
        return f'Menu for {self.date}'


class DailyMenuItem(models.Model):
    daily_menu = models.ForeignKey(
        DailyMenu, on_delete=models.CASCADE, related_name='daily_items'
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    stock = models.PositiveSmallIntegerField(default=1)

    @property
    def sold_quantity(self):
        return sum(
            item.quantity
            for item in self.order_items.filter(  # type: ignore
                order__status__in=['paid', 'in progress', 'served']
            )
        )

    @property
    def remaining_stock(self):
        return self.stock - self.sold_quantity

    @property
    def is_available(self):
        return self.stock > 0

    class Meta:
        verbose_name = 'Daily Menu Item'
        verbose_name_plural = 'Daily Menu Items'
        ordering = ('-daily_menu__date', '-stock', 'menu_item__name')

        constraints = [
            # Equivalent unique_together = ('daily_menu', 'menu_item')
            UniqueConstraint(
                fields=('daily_menu', 'menu_item'),
                name='unique_daily_menu',
                violation_error_message='Already add this menu item to the date menu',
            ),
            CheckConstraint(
                check=Q(stock__gte=0),
                name='daily_menu_item_stock_gte_0',
                violation_error_message='Stock must be greater than or equal to 0',
            ),
        ]

    def __str__(self):
        return f'{self.menu_item.name} for {self.daily_menu.date}'
