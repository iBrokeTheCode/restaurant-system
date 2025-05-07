from django.db.models import Sum
from django.shortcuts import render
from django.utils.timezone import localdate

from expenses.models import Expense
from orders.models import OrderItem
from sales.models import Sale


def reports(request):
    today = localdate()
    sales = Sale.objects.filter(payment_time__date=today)

    total_sales = sales.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = (
        Expense.objects.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0
    )

    top_sales = sales.order_by('-amount')[:5]

    top_items = (
        OrderItem.objects.filter(order__sale__payment_time__date=today)
        .values('daily_menu_item__menu_item__name')
        .annotate(quantity=Sum('quantity'))
        .order_by('-quantity')[:5]
    )

    context = {
        'date': today,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': total_sales - total_expenses,
        'top_items': top_items,
        'top_sales': top_sales,
    }
    return render(request, 'reports/reports.html', context=context)
