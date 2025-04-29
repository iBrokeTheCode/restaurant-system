from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils import timezone

from menu.models import DailyMenu, MenuCategory


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully!')
    return redirect('core:home')


def home(request):
    return render(request, 'core/home.html')


def day_menu_view(request):
    today = timezone.now().date()
    category_name = request.GET.get('category', 'Entrees')
    day_menu_items = []
    active_category = 'Entrees'

    try:
        category = MenuCategory.objects.get(name=category_name)
        active_category = category.name
    except MenuCategory.DoesNotExist:
        pass

    try:
        daily_menu = DailyMenu.objects.get(date=today)
        day_menu_items = daily_menu.daily_items.filter(  # type: ignore
            menu_item__category__name=category_name
        )
    except DailyMenu.DoesNotExist:
        pass

    context = {'menu_items': day_menu_items, 'active_category': active_category}

    return render(request, 'core/day_menu.html', context)


def tables_status_view(request):
    return render(request, 'core/tables_status.html')


@login_required()
def dashboard(request):
    return render(request, 'core/dashboard.html')
