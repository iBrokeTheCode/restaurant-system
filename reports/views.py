from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from core.mixins import DateRangeFilterMixin, GroupRequiredMixin
from expenses.models import Expense
from orders.models import OrderItem
from sales.models import Sale


class ReportView(
    LoginRequiredMixin, GroupRequiredMixin, DateRangeFilterMixin, TemplateView
):
    template_name = 'reports/reports.html'
    group_required = ['Owner']
    raise_exception = True
    date_field = 'payment_time__date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get date range from GET params
        start, end = self.get_date_range()
        date = start if start == end else f'{start} to {end}'

        # Filter and aggregate
        sales = Sale.objects.filter(payment_time__date__range=(start, end))
        total_sales = sales.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = (
            Expense.objects.filter(date__range=(start, end)).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )
        top_sales = sales.select_related('order__table').order_by('-amount')[:5]
        top_items = (
            OrderItem.objects.select_related('daily_menu_item__menu_item')
            .filter(order__sale__payment_time__date__range=(start, end))
            .values('daily_menu_item__menu_item__name')
            .annotate(quantity=Sum('quantity'))
            .order_by('-quantity')[:5]
        )

        # Update Context
        context.update(
            {
                'total_sales': total_sales,
                'total_expenses': total_expenses,
                'net_profit': total_sales - total_expenses,
                'top_items': top_items,
                'top_sales': top_sales,
                'date': date,
            }
        )
        return context
