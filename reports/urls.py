from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [path('', views.reports, name='reports-home')]
