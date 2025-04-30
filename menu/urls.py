from django.urls import path

from menu.views import (
    DailyMenuDetailView,
    DailyMenuListView,
    MenuCategoryCreateView,
    MenuCategoryDeleteView,
    MenuCategoryListView,
    MenuCategoryUpdateView,
    MenuItemCreateView,
    MenuItemDeleteView,
    MenuItemDetailView,
    MenuItemListView,
    MenuItemUpdateView,
)

app_name = 'menu'

urlpatterns = [
    path('', MenuItemListView.as_view(), name='menu-item-list'),
    path('<int:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('create/', MenuItemCreateView.as_view(), name='menu-item-create'),
    path('<int:pk>/update/', MenuItemUpdateView.as_view(), name='menu-item-update'),
    path('<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu-item-delete'),
    # Menu Category URLs
    path('category/', MenuCategoryListView.as_view(), name='menu-category-list'),
    path(
        'category/create/',
        MenuCategoryCreateView.as_view(),
        name='menu-category-create',
    ),
    path(
        'category/<int:pk>/update/',
        MenuCategoryUpdateView.as_view(),
        name='menu-category-update',
    ),
    path(
        'category/<int:pk>/delete/',
        MenuCategoryDeleteView.as_view(),
        name='menu-category-delete',
    ),
    # Daily Menu URLs
    path('daily-menu/', DailyMenuListView.as_view(), name='daily-menu-list'),
    path(
        'daily-menu/<int:pk>/', DailyMenuDetailView.as_view(), name='daily-menu-detail'
    ),
]
