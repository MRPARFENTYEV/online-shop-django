from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Product


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_avaliable = product.avaliable
    form = QuantityForm(request.POST)
    if form.is_valid() and product_avaliable == True:
        print(product)
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
        messages.success(request, 'Добавлен в корзину!', 'info')
        return redirect('shop:product_detail', slug=product.slug)
    else:
        messages.error(request,'Недоступен для заказа','error' )
        return redirect('shop:product_detail', slug=product.slug)



@login_required
def show_cart(request):
    cart = Cart(request)
    context = {'title': 'Cart', 'cart': cart}
    print(context['cart'])
    for items in context['cart']:
        print(items)
    # for items in cart:
    #     print(items)

    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:show_cart')