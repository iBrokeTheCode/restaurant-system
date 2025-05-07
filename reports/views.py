from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.timezone import localdate
from django.views.generic import TemplateView

from core.mixins import GroupRequiredMixin
from expenses.models import Expense
from orders.models import OrderItem
from sales.models import Sale


class ReportView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'reports/reports.html'
    group_required = ['Owner']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localdate()
        sales = Sale.objects.filter(payment_time__date=today)

        total_sales = sales.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = (
            Expense.objects.filter(date=today).aggregate(total=Sum('amount'))['total']
            or 0
        )

        top_sales = sales.select_related('order__table').order_by('-amount')[:5]

        top_items = (
            OrderItem.objects.select_related('daily_menu_item__menu_item')
            .filter(order__sale__payment_time__date=today)
            .values('daily_menu_item__menu_item__name')
            .annotate(quantity=Sum('quantity'))
            .order_by('-quantity')[:5]
        )

        context.update(
            {
                'date': today,
                'total_sales': total_sales,
                'total_expenses': total_expenses,
                'net_profit': total_sales - total_expenses,
                'top_items': top_items,
                'top_sales': top_sales,
            }
        )
        return context
