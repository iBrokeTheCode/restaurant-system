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

from tables.models import Table


class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'  # Default table_list


class TableDetailView(LoginRequiredMixin, DetailView):
    model = Table
    template_name = 'tables/table_detail.html'
    context_object_name = 'table'  # Default: object


class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    fields = ('table_number', 'seats', 'status')
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Table created successfully!')
        return super().form_valid(form)


class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    fields = ('table_number', 'seats', 'status')
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Table updated successfully!')
        return super().form_valid(form)


class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Table deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
