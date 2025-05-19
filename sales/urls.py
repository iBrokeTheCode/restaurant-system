from django.urls import path

from sales.views import (
    SaleCreateView,
    SaleDeleteView,
    SaleDetailView,
    SaleListView,
    SaleUpdateView,
)

app_name = 'sales'

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('create/', SaleCreateView.as_view(), name='sale-create'),
    path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('<int:pk>/delete/', SaleDeleteView.as_view(), name='sale-delete'),
]
