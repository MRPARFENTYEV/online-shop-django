from django.contrib import admin

from .models import Category, Product, Store, ProductCharacteristic, Characteristic
#
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Store)
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['title','is_sub','slug']
    list_filter = ['title','is_sub','slug']
    # list_filter = [ 'created', 'updated']


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1
@admin.register(Product)
class Category(admin.ModelAdmin):
    list_dispaly = ['category','store','title','price','date_created','slug','avaliable']
    list_filter = ['category','store','title','price','date_created','avaliable']
    inlines = [ProductCharacteristicInline,]

@admin.register(Store)
class Category(admin.ModelAdmin):
    list_display = ['title','slug']
    list_filter = ['title','slug']

# @admin.register(ProductCharacteristic)
# class Category(admin.ModelAdmin):
#     list_display = ['characteristic','product']
#     list_filter = ['characteristic','product']

# @admin.register(ProductCharacteristic)
# class Category(admin.ModelAdmin):
#     list_dispaly = ['characteristic','product']
#     list_filter = ['characteristic','product']


@admin.register(Characteristic)
class Category(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ['name','description']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug': ('title',)}
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug': ('title',)}