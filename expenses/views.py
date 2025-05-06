from calendar import monthrange

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

from core.mixins import GroupRequiredMixin
from expenses.forms import ExpenseForm
from expenses.models import Expense


class ExpenseListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    group_required = ['Owner']
    raise_exception = True

    def get_queryset(self):
        """Filter expense for the current month."""
        qs = super().get_queryset()
        today = now().date()
        first_day = today.replace(day=1)
        last_day = today.replace(day=monthrange(today.year, today.month)[1])
        return qs.filter(date__range=(first_day, last_day))

    def get_context_data(self, **kwargs):
        """Override method to pass date in the context"""
        ctx = super().get_context_data(**kwargs)
        ctx['date'] = now().date()
        return ctx


class ExpenseDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'
    group_required = ['Owner']
    raise_exception = True


class ExpenseCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')
    context_object_name = 'expense'
    group_required = ['Owner']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Expense created successfully!')
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')
    context_object_name = 'expense'
    group_required = ['Owner']
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully!')
        return super().form_valid(form)


class ExpenseDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    context_object_name = 'expense'
    success_url = reverse_lazy('expenses:expense-list')
    group_required = ['Owner']
    raise_exception = True

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Expense deleted successfully!')
        return super().delete(request, *args, **kwargs)
