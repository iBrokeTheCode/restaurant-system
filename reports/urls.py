from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [path('', views.ReportView.as_view(), name='reports-home')]
