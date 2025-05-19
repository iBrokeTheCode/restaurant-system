from django.urls import path

from expenses.views import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseListView,
    ExpenseUpdateView,
)

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
]
