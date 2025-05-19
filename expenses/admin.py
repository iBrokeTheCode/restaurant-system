from django.contrib import admin

from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date')
    list_filter = ('category',)
    search_fields = ('description',)
