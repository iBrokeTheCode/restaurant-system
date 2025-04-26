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

from sales.models import Sale


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'


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
        messages.success(self.request, 'Sale created successfully!')
        return super().form_valid(form)


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
