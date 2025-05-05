from django.contrib import admin
from django.core.exceptions import ValidationError

from core.models import BusinessInfo

admin.site.site_header = 'Restaurant System'
admin.site.site_title = 'Restaurant Admin'
admin.site.index_title = 'Home'


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'updated_at')

    def has_add_permission(self, request):
        return not BusinessInfo.objects.exists()

    def save_model(self, request, obj, form, change):
        if not change and BusinessInfo.objects.exists():
            raise ValidationError('There is already a Business Info record.')
        super().save_model(request, obj, form, change)
