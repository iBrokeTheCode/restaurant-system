from django.urls import path

from core.views import CustomLoginView, dashboard, home, logout_view

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login',
    ),
    path('logout/', logout_view, name='logout'),
]
