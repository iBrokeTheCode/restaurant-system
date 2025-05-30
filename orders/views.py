from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

from core.mixins import DateRangeFilterMixin, GroupRequiredMixin
from orders.forms import OrderForm, OrderItemForm
from orders.models import Order, OrderItem
from tables.models import TableStatusChoices

OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    form=OrderItemForm,
    extra=2,
    can_delete=True,
)


class OrderListView(
    LoginRequiredMixin, GroupRequiredMixin, DateRangeFilterMixin, ListView
):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    group_required = ['Owner', 'Cashier']
    raise_exception = True
    date_field = 'created_at__date'
    paginate_by = 5

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


class OrderDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_context_data(self, **kwargs):
        """Return to the previous filtered page or the default page."""
        context = super().get_context_data(**kwargs)
        context['previous'] = self.request.GET.get(
            'previous', reverse_lazy('orders:order-list')
        )

        return context


class OrderCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order-list')
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

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

            # Update table status to 'occupied'
            if self.object.table:
                self.object.table.status = TableStatusChoices.OCCUPIED
                self.object.table.save(update_fields=['status'])

            messages.success(self.request, 'Order created successfully!')

            return redirect(self.success_url)
        else:
            # re-render the form with errors.
            return self.render_to_response(self.get_context_data(form=form))


class OrderUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order-list')
    group_required = ['Owner', 'Cashier']
    raise_exception = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

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

        self.object = form.save(commit=False)

        if formset.is_valid():
            formset.instance = self.object
            self.object.save()
            formset.save()

            # If status changed to 'cancelled', free the table
            if self.object.status == 'cancelled' and self.object.table:
                self.object.table.status = TableStatusChoices.AVAILABLE
                self.object.table.save()

            # TODO: Case when change from CANCELLED to other status
            messages.success(self.request, 'Order updated successfully!')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class OrderDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')
    group_required = ['Owner']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Order deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
