from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    url(r'^', include('apps.register.urls')),
    path('admin/', admin.site.urls),
]