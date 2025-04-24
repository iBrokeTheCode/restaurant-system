from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from menu.models import MenuItem


class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'menu/menu_item_list.html'
    context_object_name = 'menu_items'  # Default menuitem_list


class MenuItemCreateView(CreateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default: view.object


class MenuItemUpdateView(UpdateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default view.object


class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'menu/menu_item_confirm_delete.html'
    success_url = reverse_lazy('menu:menu-item-list')
