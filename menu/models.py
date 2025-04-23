from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Menu Categories'

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, related_name='items')
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
