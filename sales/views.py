from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from sales.models import Sale


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'


class SaleCreateView(CreateView):
    model = Sale
    fields = ('order', 'payment_method')
    template_name = 'sales/sale_form.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context


class SaleUpdateView(UpdateView):
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


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales:sale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context
