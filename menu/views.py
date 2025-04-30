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

from menu.models import DailyMenu, MenuCategory, MenuItem

# ================================================================
#                           MENU ITEM
# ================================================================


class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu/menu_item_list.html'
    context_object_name = 'menu_items'  # Default: menuitem_list


class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'menu/menu_item_detail.html'
    context_object_name = 'menu_item'  # Default: object


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category', 'image')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Menu item created successfully!')
        return super().form_valid(form)


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category', 'image')
    template_name = 'menu/menu_item_form.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'  # Default: view.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Menu item updated successfully!')
        return super().form_valid(form)


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'menu/menu_item_confirm_delete.html'
    success_url = reverse_lazy('menu:menu-item-list')
    context_object_name = 'menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Menu item deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# ================================================================
#                           CATEGORIES
# ================================================================


class MenuCategoryListView(LoginRequiredMixin, ListView):
    model = MenuCategory
    template_name = 'menu/menu_category_list.html'
    context_object_name = 'menu_categories'


class MenuCategoryCreateView(LoginRequiredMixin, CreateView):
    model = MenuCategory
    fields = ('name',)
    template_name = 'menu/menu_category_form.html'
    success_url = reverse_lazy('menu:menu-category-list')
    context_object_name = 'menu_category'

    def form_valid(self, form):
        messages.success(self.request, 'Menu category created successfully!')
        return super().form_valid(form)


class MenuCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuCategory
    fields = ('name',)
    template_name = 'menu/menu_category_form.html'
    success_url = reverse_lazy('menu:menu-category-list')
    context_object_name = 'menu_category'

    def form_valid(self, form):
        messages.success(self.request, 'Menu category updated successfully!')
        return super().form_valid(form)


class MenuCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuCategory
    template_name = 'menu/menu_category_confirm_delete.html'
    success_url = reverse_lazy('menu:menu-category-list')
    context_object_name = 'menu_category'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Menu category deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# ================================================================
#                           DAILY MENU
# ================================================================


class DailyMenuListView(LoginRequiredMixin, ListView):
    model = DailyMenu
    template_name = 'menu/daily_menu_list.html'
    context_object_name = 'daily_menu'


class DailyMenuDetailView(LoginRequiredMixin, DetailView):
    model = DailyMenu
    template_name = 'menu/daily_menu_detail.html'
    context_object_name = 'daily_menu'


class DailyMenuDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyMenu
    template_name = 'menu/daily_menu_confirm_delete.html'
    success_url = reverse_lazy('menu:daily-menu-list')
    context_object_name = 'daily_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Daily Menu Item delete successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# ================================================================
#                       DAILY MENU ITEM
# ================================================================
