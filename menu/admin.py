from django.contrib import admin

from menu.models import DailyMenu, DailyMenuItem, MenuCategory, MenuItem


class DailyMenuItemInline(admin.TabularInline):
    model = DailyMenuItem
    extra = 3


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    search_fields = ('date',)
    inlines = (DailyMenuItemInline,)


@admin.register(DailyMenuItem)
class DailyMenuItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'daily_menu', 'stock', 'sold_quantity')
    list_filter = ('daily_menu__date',)
    search_fields = ('daily_menu__date',)
