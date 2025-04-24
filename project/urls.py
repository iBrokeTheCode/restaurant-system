from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

DJANGO_URLS = [
    path('admin/', admin.site.urls),
]

THIRD_PARTY_URLS = [] + debug_toolbar_urls()


LOCAL_URLS = [
    path('', include('core.urls', namespace='core')),
    path('menu/', include('menu.urls', namespace='menu')),
    path('tables/', include('tables.urls', namespace='tables')),
]

urlpatterns = DJANGO_URLS + THIRD_PARTY_URLS + LOCAL_URLS
