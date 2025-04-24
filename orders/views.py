from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from orders.models import Order, OrderItem

OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    fields=('menu_item', 'quantity', 'unit_price', 'note'),
    extra=1,
    can_delete=True,
)


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    fields = ('table', 'status')
    template_name = 'orders/order_form.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save order
            self.object = form.save()
            # Assign it as the parent of order items formset
            formset.instance = self.object
            # Save formset
            formset.save()
            return redirect(self.success_url)
        else:
            # re-render the form with errors.
            return self.render_to_response(self.get_context_data(form=form))


class OrderUpdateView(UpdateView):
    model = Order
    fields = ('table', 'status')
    template_name = 'orders/order_form.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = OrderItemFormSet(
                self.request.POST, instance=self.get_object()
            )
        else:
            context['formset'] = OrderItemFormSet(instance=self.get_object())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


# TODO: Go back to previous page (use next url param)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')
