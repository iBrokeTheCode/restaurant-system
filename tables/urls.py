from django.urls import path

from tables.views import (
    TableCreateView,
    TableDeleteView,
    TableDetailView,
    TableListView,
    TableUpdateView,
)

app_name = 'tables'

urlpatterns = [
    path('', TableListView.as_view(), name='table-list'),
    path('<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    path('create/', TableCreateView.as_view(), name='table-create'),
    path('<int:pk>/update/', TableUpdateView.as_view(), name='table-update'),
    path('<int:pk>/delete/', TableDeleteView.as_view(), name='table-delete'),
]
