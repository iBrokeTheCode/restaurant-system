from django.urls import path

from expenses.views import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseListView,
)

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
]
