from django.contrib import admin

from tables.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'seats', 'status')
    list_filter = ('status',)
    search_fields = ('table_number',)
