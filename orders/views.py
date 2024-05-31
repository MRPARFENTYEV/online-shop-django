from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from accounts.models import Contact, User
from accounts.views import user_register
from online_shop.settings import EMAIL_HOST_USER
from shop.models import Product, Store
from .models import Order, OrderItem
from cart.utils.cart import Cart



def not_enough_quantity(request):
    context = {'Not_enough': 'Товара недостаточно'}
    return render(request, 'not_enough_quantity.html', context)

def no_way_to_order(request):
    context={'order':'order'}
    return render(request,'no_way_to_order.html',context)

def manager_contact(cart):
    for item in cart:
        products_data = Product.objects.filter(slug=item['product'])
        for product in products_data:
            store_id = product.store_id
            store = Store.objects.get(id=store_id)
            manager = User.objects.get(store_name = store.title)
            return(manager.email)



# def enough_quant
def product_quantity(item):
    products_data = Product.objects.filter(slug=item['product'])
    for product in products_data:
        old_quontity = product.quantity
        # print('old_quontity',old_quontity)
        product.quantity = product.quantity - item['quantity']
        product.save()
        # print('product.quantity',product.quantity)
        return old_quontity >= item['quantity']

@login_required
def create_order(request):
    user = request.user

    cart = Cart(request)
    # print(manager_contact(cart))

    order = Order.objects.create(user=request.user)
    for item in cart:
        # product_quantity(item)
        # print(product_quantity(item))
        if product_quantity(item) == True:

            OrderItem.objects.create(
                order=order, product=item['product'],
                price=item['price'], quantity=item['quantity']
        )
    send_mail('Онлайн магазин - Потный айтишник',
                          f'Уважаемый Потный айтишник, Ваш заказ создан: {order}', EMAIL_HOST_USER, [request.user.email])
    send_mail('Онлайн магазин - Потный айтишник',
              f'Уважаемый Потный менеджер, заказ создан, начинайте собирать: {order}', EMAIL_HOST_USER, [manager_contact(cart)])


    return redirect('orders:pay_order', order_id=order.id)


def order_detail(request, order_id):
    order = request.user.orders.get(id=order_id)
    orderitem=OrderItem.objects.filter(order_id=order.id)
    addresses = Contact.objects.filter(user_id=request.user.pk)
    # order = Order.objects.get(id=order_id)
    context={'order':order,'orderitem':orderitem, 'addresses' :addresses }
    return render(request,'order_detail.html',context)
# @login_required
# def create_order(request):
#     user_verification = request.user.email_verify
#     print(user_verification)
#     if user_verification:
#         cart = Cart(request)
#         order = Order.objects.create(user=request.user)
#         for item in cart:
#             OrderItem.objects.create(
#                 order=order, product=item['product'],
#                 price=item['price'], quantity=item['quantity']
#         )
#             return redirect('orders:pay_order', order_id=order.id)

# @login_required
# def create_order(request):
#     cart = Cart(request)
#     order = Order.objects.create(user=request.user)
#     for item in cart:
#         OrderItem.objects.create(
#             order=order, product=item['product'],
#             price=item['price'], quantity=item['quantity']
#         )
#     return redirect('orders:pay_order', order_id=order.id)

            # listus =[]
#             print(listus)
#             product_get = Product.objects.filter(slug=item['product'])
#             for prod in product_get:
# # print('prod',prod)
#                 print('prod.quantity',prod.quantity)
#                 print('item[product]',item['product'])
#                 print('item[quantity]',item['quantity'])
#                 print(prod.quantity > item['quantity'])
# @login_required
# def create_order(request):
#     user_verification = request.user.email_verify
#     if user_verification:
#
#         cart = Cart(request)
#         order = Order.objects.create(user=request.user)
#
#         for item in cart:
#             print('item', item)
#             # product_get = Product.objects.filter(slug=item['product'])
#             # print('product_get', product_get)
#             # OrderItem.objects.create(
#             #     order=order, product=item['product'],
#             #     price=item['price'], quantity=item['quantity']
#             # )
#             # store = Store.objects.get(id=product_get.store_id)
#             # managers = User.objects.filter(store_name=store.title)
#
#
#             # product_get_quantity = product_get.quantity
#             # if item['quantity'] > product_get_quantity:
#             #     return not_enough_quantity(request)
#             # else:
#             #     OrderItem.objects.create(
#             #         order=order, product=item['product'],
#             #         price=item['price'], quantity=item['quantity']
#             # )
#             # product_get.quantity = product_get.quantity - item['quantity']
#             # product_get.save()
#             # send_mail('Онлайн магазин - Потный айтишник',
#             #           f'Уважаемый Потный айтишник, Ваш заказ создан: {order}', EMAIL_HOST_USER, [request.user.email])
#             # for manager in managers:
#             #     send_mail('Онлайн магазин - Потный айтишник',
#             #               f'Уважаемый Потный менеджер, заказ ожидает исполнения. Подробнее тут: http://127.0.0.1:8000/see_orders/ {order}', EMAIL_HOST_USER, [manager.email])
#
#
#             return redirect('orders:pay_order', order_id=order.id)
#     else:
#         user_register(request)


# @login_required
# def create_order(request):
#     cart = Cart(request)
#     # order = Order.objects.create(user=request.user)
#     # # products = Product.objects.filter(avaliable=False)
#     # products = Product.objects.filter(avaliable=False)
#     for item in cart:
#         product_get = Product.objects.get(slug=item['product'])
#         products = Product.objects.filter(avaliable=False)
#         print(product_get)
#         product_get_quantity = product_get.quantity
#         return redirect('orders:no_way_to_order')

        #
        # if item['quantity'] > product_get_quantity:
        #     return not_enough_quantity(request)
        # else:
        #     OrderItem.objects.create(
        #         order=order, product=item['product'],
        #         price=item['price'], quantity=item['quantity']
        # )
    # print(products)
    # if products:
    #     for product in products:
    #         product_slug = product.slug
    #         print('________________________________________________',product_slug)
    #
    #         for item in cart:
    #             product_get = Product.objects.get(slug=item['product'])
    #             product_get_quantity = product_get.quantity
    #         print("++++++++++++++++++++",product_get.slug)
            # print(str(product_slug)==str(product_get))
    # if str(product_slug)==str(product_get):
    #     print("jjkjk")
        #     return redirect('orders:no_way_to_order')
        # else:
        #     # product_get = Product.objects.get(slug=item['product'])
        #     # product_get_quantity = product_get.quantity
        #
        #     if item['quantity'] > product_get_quantity:
        #         return not_enough_quantity(request)
        #     else:
        #         OrderItem.objects.create(
        #             order=order, product=item['product'],
        #             price=item['price'], quantity=item['quantity']
        #     )
        #
        #     product_get.quantity = product_get.quantity - item['quantity']
        #     product_get.save()
        #     send_mail('Онлайн магазин - Потный айтишник',
        #               f'Уважаемый Потный айтишник, Ваш заказ создан: {order}', EMAIL_HOST_USER, [request.user.email])

                # .update(quantity=Product.quantity - item['quantity'])
        # return redirect('orders:pay_order', order_id=order.id)



    # product_quantity = OrderItem.objects
    # for product in products:

    #         for item in cart:
    #             print(item)
    #             product_get = Product.objects.get(slug=item['product'])
    #             product_get_quantity = product_get.quantity
    #
    #             if item['quantity'] > product_get_quantity:
    #                 return not_enough_quantity(request)
    #             else:
    #                 OrderItem.objects.create(
    #                     order=order, product=item['product'],
    #                     price=item['price'], quantity=item['quantity']
    #             )
    #             product_get.quantity = product_get.quantity - item['quantity']
    #             product_get.save()
    #
    #                 # .update(quantity=Product.quantity - item['quantity'])
    #             return redirect('orders:pay_order', order_id=order.id)
    #     else:



@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order}
    return render(request, 'checkout.html', context)


@login_required
def fake_payment(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()
    send_mail('Онлайн магазин - Потный айтишник',
              f'Уважаемый Потный айтишник, Ваш заказ оплачен: {order}, '
              f' его можно посмотреть на сайте "Потный айтишник в профеле > Заказы или по ссылке: http://127.0.0.1:8000/orders/list '
              , EMAIL_HOST_USER, [request.user.email])
    send_mail('Онлайн магазин - Потный айтишник',
              f'Уважаемый Потный менеджер, заказ оплачен, начинайте доставлять: {order}', EMAIL_HOST_USER,
              [manager_contact(cart)])
    # send_mail('Онлайн магазин - Потный айтишник', )
    return redirect('orders:user_orders')


@login_required
def user_orders(request):
    user = request.user
    orders = request.user.orders.all()
    # print(orders)
    # print(type(orders))
    addresses = Contact.objects.filter(user_id =request.user.pk )
    for order in orders:
        last_order = order
    for address in addresses:
        user_adress = address
    if addresses:
        context = {'title': 'Orders', 'orders': orders, 'adresses': address}

        return render(request, 'user_orders.html', context)
    #
    else:
        return redirect('accounts:contact')


