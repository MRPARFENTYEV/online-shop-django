from django.urls import path
from django.conf.global_settings import DEFAULT_CHARSET
from shop import views

app_name = "shop"

urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('<slug:slug>', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
	path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
	path('filter_by_store/<slug:slug>/', views.filter_by_store, name='filter_by_store'),
	path('characteristics/<slug:slug>/',views.list_characteristics,name='characteristics'),
	path('update_prices/', views.update_prices, name='update_prices' ),
	path('go_away/', views.go_away, name='go_away'),
	path('see_orders/',views.get_orders, name='see_orders' )

]
# C:\Users\mrpar\Shop_python\price_operations\prices_update.xlsx