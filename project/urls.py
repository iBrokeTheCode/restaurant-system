from django.contrib import admin
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

DJANGO_URLS = [
    path('admin/', admin.site.urls),
]

THIRD_PARTY_URLS = [] + debug_toolbar_urls()


LOCAL_URLS = [
    path('', include('core.urls', namespace='core')),
]

urlpatterns = DJANGO_URLS + THIRD_PARTY_URLS + LOCAL_URLS
