from django.contrib import admin

from menu.models import MenuCategory, MenuItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)
