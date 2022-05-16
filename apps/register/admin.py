from django.contrib import admin

# Register your models here.
from .models import User
# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(User)