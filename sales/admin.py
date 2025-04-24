from django.contrib import admin

from sales.models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'amount', 'payment_time')
    list_filter = ('payment_method',)
    search_fields = ('order__id',)
