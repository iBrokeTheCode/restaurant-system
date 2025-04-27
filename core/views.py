from datetime import date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from menu.models import DailyMenu


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
    today = date.today()
    daily_menu = DailyMenu.objects.filter(date=today).first()
    menu_items = daily_menu.menu_items.all() if daily_menu else None

    context = {
        'daily_menu': daily_menu,
        'menu_items': menu_items,
    }

    return render(request, 'core/day_menu.html', context=context)


def tables_status_view(request):
    return render(request, 'core/tables_status.html')


@login_required()
def dashboard(request):
    return render(request, 'core/dashboard.html')
