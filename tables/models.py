from django.db import models

from django.core.validators import MinValueValidator


class Table(models.Model):
    class TableStatusChoices(models.TextChoices):
        AVAILABLE = ('available', 'Available')
        OCCUPIED = ('occupied', 'Occupied')
        RESERVED = ('reserved', 'Reserved')

    table_number = models.PositiveSmallIntegerField(unique=True)
    seats = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10, choices=TableStatusChoices, default=TableStatusChoices.AVAILABLE)

    def __str__(self) -> str:
        return f'Table #{self.table_number}'
