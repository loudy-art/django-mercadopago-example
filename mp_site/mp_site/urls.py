#mp_site URL Configuration

from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path("payments/", include("payments.urls")),
    path('', include('pagos.urls')),
]

