from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)


@admin.action(description='Mark selected orders as served')
def mark_as_served(modeladmin, request, queryset):
    queryset.update(status=Order.OrderStatusChoices.SERVED)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('table', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('table__table_number',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    actions = [mark_as_served]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'daily_menu_item', 'quantity', 'unit_price', 'total_price')
    search_fields = ('daily_menu_item__menu_item__name',)
