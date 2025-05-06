from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from orders.models import Order
from sales.models import Sale
from tables.models import TableStatusChoices


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'

    def get_queryset(self):
        """Filter sales for the current day."""
        qs = super().get_queryset()
        today = now().date()
        return qs.filter(payment_time__date=today)

    def get_context_data(self, **kwargs):
        """Override method to pass date in the context."""
        ctx = super().get_context_data(**kwargs)
        ctx['date'] = now().date()
        return ctx


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    fields = ('order', 'payment_method')
    template_name = 'sales/sale_form.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')

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


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = Sale
    fields = ('order', 'amount', 'payment_method')
    template_name = 'sales/sale_form.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')

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


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sale deleted successfully!')

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
