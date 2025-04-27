from django.contrib import admin

from core.models import BusinessInfo

admin.site.site_header = 'Restaurant System'
admin.site.site_title = 'Restaurant Admin'
admin.site.index_title = 'Home'


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'updated_at')
