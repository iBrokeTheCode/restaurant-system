from django.urls import path

from menu.views import (
    MenuItemListView,
    MenuItemCreateView,
    MenuItemUpdateView,
    MenuItemDeleteView
)

app_name = 'menu'

urlpatterns = [
    path('', MenuItemListView.as_view(), name='menu-item-list'),
    path('create/', MenuItemCreateView.as_view(), name='menu-item-create'),
    path('<int:pk>/update/', MenuItemUpdateView.as_view(), name='menu-item-update'),
    path('<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu-item-delete')
]
