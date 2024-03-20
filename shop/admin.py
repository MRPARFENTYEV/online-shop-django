from django.contrib import admin

from .models import Category, Product, Store

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Store)
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug': ('title',)}
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug': ('title',)}