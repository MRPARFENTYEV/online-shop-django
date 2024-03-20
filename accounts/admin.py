from django.contrib import admin

from .models import User

admin.site.register(User)
# search_fields = ['full_name']