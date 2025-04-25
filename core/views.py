from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'core/home.html')


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_url = 'core:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_url)
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('core:home')
