from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from accounts.models import Contact
from shop.models import Product
from .models import Order, OrderItem
from cart.utils.cart import Cart

def not_enough_quantity(request):
    context = {'Not_enough': 'Товара недостаточно'}
    print('not_enough_quantity',request)
    return render(request, 'not_enough_quantity.html', context)

def no_way_to_order(request):
    context={'order':'order'}
    return render(request,'no_way_to_order.html',context)

@login_required
def create_order(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    products = Product.objects.filter(avaliable=False)
    for product in products:
        product_slug = product.slug
        print(product_slug)
    for item in cart:
        product_get = Product.objects.get(slug=item['product'])
        product_get_quantity = product_get.quantity
        # print(product_get)
        # print(str(product_slug)==str(product_get))
        if str(product_slug)==str(product_get):
            return redirect('orders:no_way_to_order')
        else:
            # product_get = Product.objects.get(slug=item['product'])
            # product_get_quantity = product_get.quantity

            if item['quantity'] > product_get_quantity:
                return not_enough_quantity(request)
            else:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity']
            )
            product_get.quantity = product_get.quantity - item['quantity']
            product_get.save()

                # .update(quantity=Product.quantity - item['quantity'])
            return redirect('orders:pay_order', order_id=order.id)



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
    return redirect('orders:user_orders')


@login_required
def user_orders(request):
    orders = request.user.orders.all()
    addresses = Contact.objects.filter(user_id =request.user.pk )
    for address in addresses:
        user_adress = address
    if addresses:
        context = {'title': 'Orders', 'orders': orders, 'adresses': address}
        return render(request, 'user_orders.html', context)
    #
    else:
        return redirect('accounts:contact')


