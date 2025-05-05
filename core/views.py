from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils import timezone

from menu.models import DailyMenu, MenuCategory
from tables.models import Table


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('core:home')


def home(request):
    return render(request, 'core/home.html')


def day_menu_view(request):
    today = timezone.now().date()
    categories = MenuCategory.objects.all()
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

    context = {
        'active_category': active_category,
        'categories': categories,
        'menu_items': day_menu_items,
    }

    return render(request, 'core/day_menu.html', context)


def tables_status_view(request):
    context = {
        'tables': Table.objects.all().order_by('table_number'),
        'last_update': timezone.now(),
    }
    return render(request, 'core/tables_status.html', context)


@login_required()
def dashboard(request):
    return render(request, 'core/dashboard.html')
