from django.urls import path

from menu.views import (
    DailyMenuCreateView,
    DailyMenuDeleteView,
    DailyMenuDetailView,
    DailyMenuItemCreateView,
    DailyMenuItemDeleteView,
    DailyMenuItemDetailView,
    DailyMenuItemListView,
    DailyMenuItemUpdateView,
    DailyMenuListView,
    DailyMenuUpdateView,
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
    # Menu Item URLs
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
    path('daily-menu/create/', DailyMenuCreateView.as_view(), name='daily-menu-create'),
    path(
        'daily-menu/<int:pk>/update/',
        DailyMenuUpdateView.as_view(),
        name='daily-menu-update',
    ),
    path(
        'daily-menu/<int:pk>/delete',
        DailyMenuDeleteView.as_view(),
        name='daily-menu-delete',
    ),
    # Daily Menu Item URLs
    path(
        'daily-menu-item/', DailyMenuItemListView.as_view(), name='daily-menu-item-list'
    ),
    path(
        'daily-menu-item/<int:pk>/',
        DailyMenuItemDetailView.as_view(),
        name='daily-menu-item-detail',
    ),
    path(
        'daily-menu-item/create/',
        DailyMenuItemCreateView.as_view(),
        name='daily-menu-item-create',
    ),
    path(
        'daily-menu-item/<int:pk>/update/',
        DailyMenuItemUpdateView.as_view(),
        name='daily-menu-item-update',
    ),
    path(
        'daily-menu-item/<int:pk>/delete',
        DailyMenuItemDeleteView.as_view(),
        name='daily-menu-item-delete',
    ),
]
