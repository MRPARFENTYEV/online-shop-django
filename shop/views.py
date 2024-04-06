from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.forms import StoreTitleForm, ProductForm
from shop.models import Product, Category, Store, Characteristic, ProductCharacteristic
from cart.forms import QuantityForm
import pandas as pd
from online_shop.settings import EMAIL_HOST_USER
from django.forms import ModelForm
def paginat(request, list_objects):# https://docs.djangoproject.com/en/5.0/topics/pagination/

	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj

def go_away(request):
	context = {'context':'вернитесь'}
	return render(request, 'go_away.html',context )

def home_page(request):
	user = request.user
	print(user)
	if not hasattr(request.user, 'is_manager'):
		products = Product.objects.filter(avaliable=True)
		context = {'products': paginat(request,products)}  # тут в пагинатор приходит запрос и продукты передаются в виде списка
		return render(request, 'home_page.html', context)

	if user.is_manager:
		products = Product.objects.all()
		context = {'products': paginat(request ,products)} # тут в пагинатор приходит запрос и продукты передаются в виде списка
		return render(request, 'home_page.html', context)
	else:
		products = Product.objects.filter(avaliable=True)
		context = {'products': paginat(request,products)}  # тут в пагинатор приходит запрос и продукты передаются в виде списка
		return render(request, 'home_page.html', context)



def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	related_products = Product.objects.filter(category=product.category).all()[:5]
	products = Product.objects.filter(slug=slug).first()# вывод характеристик
	avaliable = ProductForm(request.POST, instance=product)

	store = Store.objects.get(pk=product.store_id)

	context = {
		'title': product.title,
		'product': product,
		'form': form,
		'store': product.store,
		'favorites': 'favorites',
		'related_products': related_products,
		'products': products,  # это добавляемые поля(параметры)
		'avaliable': avaliable
	}


	if not hasattr(request.user, 'is_manager'):
		anonimus_user = request.user

		return render(request, 'product_detail.html', context)
	if hasattr(request.user, 'is_manager'):
		if request.user.is_manager == True and request.user.store_name == store.title:

			manager = request.user.is_manager
			if manager:
				if avaliable.is_valid():
					avaliable.save()
				return render(request, 'product_detail_manager.html', context)
		if request.user.is_manager == False:
			user = request.user

	if request.user.likes.filter(id=product.id).first():
		context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)
	# return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)


def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
	"""когда пользователь кликает на род. категорию , ему показываются также все продукты в ее внутреннем классе.
	"""
	result = []
	category = Category.objects.filter(slug=slug).first()

	[result.append(product) \
		for product in Product.objects.filter(category=category.id).all()]

	# check if category is parent then get all sub-categories
	if not category.is_sub:
		sub_categories = category.sub_categories.all()
		# get all sub-categories products 
		for category in sub_categories:
			[result.append(product) \
				for product in Product.objects.filter(category=category).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'home_page.html', context)

def filter_by_store(request, slug):
	print(slug)

	result = []
	store = Store.objects.filter(slug=slug).first()
	print(store)
	[result.append(product) \
		for product in Product.objects.filter(store=store.id).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'home_page.html', context)

def list_characteristics(request,slug):

    # characteristics = Characteristic.objects.all()
	products = Product.objects.filter(slug=slug).first()
    # context = {'characteristics':characteristics}
	context = {'products':products }
	return render(request,'characteristics.html',context)
	# return render(request,products)

def writing_from_file(request, title, price):
	print(title)
	products = Product.objects.filter(title=title).update(price=price)

def update_prices(request):
	user_name = request.user.full_name
	user = request.user
	user_store_name = user.store_name
	# store = Store.objects.get(title=user_store_name)
	manager = request.user.is_manager
	user = request.user.full_name
	if manager:
		print(manager)
		if request.POST:
			file = request.FILES['myfile']
			data = pd.read_excel(file)
			for price, title in zip(data['price'], data['title']):
				writing_from_file(request, title, price)
				context = {'text': 'text', 'user': user, 'user_store': user_store_name}

				return render(request, 'update_prices.html', context)
		else:


			context = {'text': 'text', 'user': user, 'user_store': user_store_name}

			return render(request, 'update_prices.html', context)

	else:
			store = 'Вы не закреплены ни за одним магазином осуществляющим продажу на платформе "Потный айтишник". Уходите...'
			context = {'text': 'text', 'user': user_name, 'user_store': store}
			return render(request, 'update_prices.html', context)


