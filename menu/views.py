from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from menu.forms import DailyMenuForm
from menu.models import DailyMenu, DailyMenuItem, MenuCategory, MenuItem

# ================================================================
#                           MENU ITEM
# ================================================================


class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu/menu_item/menu_item_list.html'
    context_object_name = 'menu_items'  # Default: menuitem_list


class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'menu/menu_item/menu_item_detail.html'
    context_object_name = 'menu_item'  # Default: object


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    fields = ('name', 'description', 'price', 'category', 'image')
    template_name = 'menu/menu_item/menu_item_form.html'
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
    template_name = 'menu/menu_item/menu_item_form.html'
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
    template_name = 'menu/menu_item/menu_item_confirm_delete.html'
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
    template_name = 'menu/menu_category/menu_category_list.html'
    context_object_name = 'menu_categories'


class MenuCategoryCreateView(LoginRequiredMixin, CreateView):
    model = MenuCategory
    fields = ('name',)
    template_name = 'menu/menu_category/menu_category_form.html'
    success_url = reverse_lazy('menu:menu-category-list')
    context_object_name = 'menu_category'

    def form_valid(self, form):
        messages.success(self.request, 'Menu category created successfully!')
        return super().form_valid(form)


class MenuCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuCategory
    fields = ('name',)
    template_name = 'menu/menu_category/menu_category_form.html'
    success_url = reverse_lazy('menu:menu-category-list')
    context_object_name = 'menu_category'

    def form_valid(self, form):
        messages.success(self.request, 'Menu category updated successfully!')
        return super().form_valid(form)


class MenuCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuCategory
    template_name = 'menu/menu_category/menu_category_confirm_delete.html'
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

DailyMenuItemFormSet = inlineformset_factory(
    parent_model=DailyMenu,
    model=DailyMenuItem,
    fields=('menu_item', 'stock'),
    extra=1,
    can_delete=True,
)


class DailyMenuListView(LoginRequiredMixin, ListView):
    model = DailyMenu
    template_name = 'menu/daily_menu/daily_menu_list.html'
    context_object_name = 'daily_menu'


class DailyMenuDetailView(LoginRequiredMixin, DetailView):
    model = DailyMenu
    template_name = 'menu/daily_menu/daily_menu_detail.html'
    context_object_name = 'daily_menu'


class DailyMenuCreateView(LoginRequiredMixin, CreateView):
    model = DailyMenu
    form_class = DailyMenuForm
    template_name = 'menu/daily_menu/daily_menu_form.html'
    context_object_name = 'daily_menu'
    success_url = reverse_lazy('menu:daily-menu-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        if self.request.POST:
            context['formset'] = DailyMenuItemFormSet(self.request.POST)
        else:
            context['formset'] = DailyMenuItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Daily Menu created successfully!')

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DailyMenuUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyMenu
    form_class = DailyMenuForm
    template_name = 'menu/daily_menu/daily_menu_form.html'
    context_object_name = 'daily_menu'
    success_url = reverse_lazy('menu:daily-menu-list')

    def get_success_url(self):
        next_url = self.request.GET.get('next')

        return next_url if next_url else super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)

        if self.request.POST:
            context['formset'] = DailyMenuItemFormSet(
                self.request.POST, instance=self.get_object()
            )
        else:
            context['formset'] = DailyMenuItemFormSet(instance=self.get_object())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Daily Menu created successfully!')

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DailyMenuDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyMenu
    template_name = 'menu/daily_menu/daily_menu_confirm_delete.html'
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


class DailyMenuItemListView(LoginRequiredMixin, ListView):
    model = DailyMenuItem
    template_name = 'menu/daily_menu_item/daily_menu_item_list.html'
    context_object_name = 'daily_menu_items'

    def get_queryset(self):
        today = now().date()
        return DailyMenuItem.objects.filter(daily_menu__date=today)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = now().date()
        return context


class DailyMenuItemDetailView(LoginRequiredMixin, DetailView):
    model = DailyMenuItem
    template_name = 'menu/daily_menu_item/daily_menu_item_detail.html'
    context_object_name = 'daily_menu_item'


class DailyMenuItemCreateView(LoginRequiredMixin, CreateView):
    model = DailyMenuItem
    fields = ('daily_menu', 'menu_item', 'stock')
    template_name = 'menu/daily_menu_item/daily_menu_item_form.html'
    success_url = reverse_lazy('menu:daily-menu-item-list')
    context_object_name = 'daily_menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Daily Menu item created successfully!')
        return super().form_valid(form)


class DailyMenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyMenuItem
    fields = ('daily_menu', 'menu_item', 'stock')
    template_name = 'menu/daily_menu_item/daily_menu_item_form.html'
    success_url = reverse_lazy('menu:daily-menu-item-list')
    context_object_name = 'daily_menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Daily Menu item updated successfully!')
        return super().form_valid(form)


class DailyMenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyMenuItem
    template_name = 'menu/daily_menu_item/daily_menu_item_confirm_delete.html'
    success_url = reverse_lazy('menu:daily-menu-item-list')
    context_object_name = 'daily_menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.success_url)
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Daily Menu Item delete successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
