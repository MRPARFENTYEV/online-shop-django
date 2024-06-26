from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('create', views.create_order, name='create_order'),
    path('list', views.user_orders, name='user_orders'),
    path('checkout/<int:order_id>', views.checkout, name='checkout'),
    path('fake-payment/<int:order_id>', views.fake_payment, name='pay_order'),
    path('no_way_to_order', views.no_way_to_order, name='no_way_to_order'),
    # path('not_enough_quantity',views.not_enough_quantity, name='not_enough_quantity')
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail')

]