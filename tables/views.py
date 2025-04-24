from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from tables.models import Table


class TableListView(ListView):
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'


class TableDetailView(DetailView):
    model = Table
    template_name = 'tables/table_detail.html'
    context_object_name = 'table'  # Default: object


class TableCreateView(CreateView):
    model = Table
    fields = ('table_number', 'seats', 'status')
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: view.object


class TableUpdateView(UpdateView):
    model = Table
    fields = ('table_number', 'seats', 'status')
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)


class TableDeleteView(DeleteView):
    model = Table
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('tables:table-list')
    context_object_name = 'table'  # Default: object
