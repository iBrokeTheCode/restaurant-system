from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from expenses.models import Expense


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    context_object_name = 'expense'
    success_url = reverse_lazy('expenses:expense-list')


class ExpenseCreateView(CreateView):
    model = Expense
    fields = ('amount', 'description', 'category', 'date')
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')
    context_object_name = 'expense'
