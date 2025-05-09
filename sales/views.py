from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from core.mixins import DateRangeFilterMixin, GroupRequiredMixin
from orders.models import Order
from sales.models import Sale
from tables.models import TableStatusChoices


class SaleListView(
    LoginRequiredMixin, GroupRequiredMixin, DateRangeFilterMixin, ListView
):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    group_required = ['Owner', 'Cashier']
    raise_exception = True
    date_field = 'payment_time__date'

    def get_queryset(self):
        """Filter sales for the selected date range."""
        qs = super().get_queryset()
        return self.filter_queryset_by_date(qs)

    def get_context_data(self, **kwargs):
        """Override method to pass date in the context."""
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        start, end = self.get_date_range()
        date = start if start == end else f'{start} to {end}'

        context.update({'date': date})
        return context


class SaleDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_context_data(self, **kwargs):
        """Return to the previous filtered page or the default page."""
        context = super().get_context_data(**kwargs)
        context['previous'] = self.request.GET.get(
            'previous', reverse_lazy('sales:sale-list')
        )

        return context


class SaleCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Sale
    fields = ('order', 'payment_method')
    template_name = 'sales/sale_form.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def form_valid(self, form):
        # Change tables status to available
        response = super().form_valid(form)
        order = form.cleaned_data.get('order')

        if order:
            # Update order status
            order.status = Order.OrderStatusChoices.PAID
            order.save()

            # Update table status
            table = order.table
            if table:
                table.status = TableStatusChoices.AVAILABLE
                table.save()

        messages.success(self.request, 'Sale created successfully!')

        return response

    def get_initial(self):
        initial = super().get_initial()
        order_id = self.request.GET.get('order_id')
        if order_id:
            initial['order'] = Order.objects.filter(pk=order_id).first()
        return initial


class SaleUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Sale
    fields = ('order', 'amount', 'payment_method')
    template_name = 'sales/sale_form.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

    def form_valid(self, form):
        messages.success(self.request, 'Sale updated successfully!')
        return super().form_valid(form)


class SaleDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')
    group_required = ['Owner']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sale deleted successfully!')

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
