from django.contrib import admin
from .models import Order

# admin.site.register
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','created','updated','status']
    list_filter = ['user','created','updated','status']

