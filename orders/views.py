from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from orders.models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    pass


class OrderUpdateView(UpdateView):
    pass


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')
