from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'core/home.html')


def dashboard(request):
    return render(request, 'core/dashboard.html')


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    return redirect('core:home')
