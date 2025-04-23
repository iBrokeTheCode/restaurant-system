from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint


class Expense(models.Model):
    class CategoryChoice(models.TextChoices):
        INVENTORY = ('inventory', 'Inventory')
        SALARY = ('salary', 'Salary')
        MAINTENANCE = ('maintenance', 'Maintenance')
        OTHER = ('other', 'Other')

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[
                                 MinValueValidator(0.01)])
    category = models.CharField(
        max_length=20, choices=CategoryChoice, default=CategoryChoice.INVENTORY)
    date = models.DateField()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(amount__gt=0), name='expense_amount_gt_0')
        ]

    def __str__(self) -> str:
        return f'{self.description} - S/.{self.amount} on {self.date}'
