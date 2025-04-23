from django.db import models

from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint


class Table(models.Model):
    class TableStatusChoices(models.TextChoices):
        AVAILABLE = ('available', 'Available')
        OCCUPIED = ('occupied', 'Occupied')
        RESERVED = ('reserved', 'Reserved')

    table_number = models.PositiveSmallIntegerField(unique=True)
    seats = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10, choices=TableStatusChoices, default=TableStatusChoices.AVAILABLE)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(seats__gte=1), name='table_seats_gte_1')
        ]

    def __str__(self) -> str:
        return f'Table #{self.table_number}'
