from django.urls import path

from core.views import (
    CustomLoginView,
    dashboard,
    day_menu_view,
    home,
    logout_view,
    tables_status_view,
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('day-menu/', day_menu_view, name='day-menu'),
    path('tables-status/', tables_status_view, name='tables-status'),
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login',
    ),
    path('logout/', logout_view, name='logout'),
]
