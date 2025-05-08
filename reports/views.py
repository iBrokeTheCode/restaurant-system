from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.timezone import datetime, localdate, timedelta
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

        request = self.request
        range_type = request.GET.get('range', 'today')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        today = localdate()

        start = end = today  # Default fallback

        if range_type == 'week':
            start = today - timedelta(days=today.weekday())  # Monday
            end = today

        elif range_type == 'month':
            start = today.replace(day=1)
            end = today

        elif range_type == 'custom':
            try:
                if start_date and end_date:
                    start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end = datetime.strptime(end_date, '%Y-%m-%d').date()
                    if start > end:
                        raise ValueError('Start date is after end date.')
                else:
                    raise ValueError('Missing dates.')
            except ValueError:
                messages.warning(
                    request, "Invalid custom date range. Showing today's data."
                )
                start = end = today

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

        context.update(
            {
                'start': start,
                'end': end,
                'total_sales': total_sales,
                'total_expenses': total_expenses,
                'net_profit': total_sales - total_expenses,
                'top_items': top_items,
                'top_sales': top_sales,
            }
        )
        return context
