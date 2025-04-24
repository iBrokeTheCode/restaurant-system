from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from menu.models import MenuItem


class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'menu/menu_item_list.html'
    context_object_name = 'menu_items'  # Default menuitem_list


class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'menu/menu_item_detail.html'
    context_object_name = 'menu_item'


class MenuItemCreateView(CreateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context


class MenuItemUpdateView(UpdateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)


class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'menu/menu_item_confirm_delete.html'
    success_url = reverse_lazy('menu:menu-item-list')
