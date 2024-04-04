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
	products = Product.objects.all()
	context = {'products': paginat(request ,products)} # тут в пагинатор приходит запрос и продукты передаются в виде списка
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	related_products = Product.objects.filter(category=product.category).all()[:5]
	products = Product.objects.filter(slug=slug).first()# вывод характеристик
	context = {
		'title':product.title,
		'product':product,
		'form':form,
		'store': product.store,
		'favorites':'favorites',
		'related_products':related_products,
		'products': products # это добавляемые поля(параметры)
	}
	print(context['products'])
	anonimus_user = request.user
	if str(anonimus_user) == 'AnonymousUser':
		return render(request, 'product_detail.html', context)

	else:

		if request.user.likes.filter(id=product.id).first():
			context['favorites'] = 'remove'



	return render(request, 'product_detail.html', context)


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
	print(category)
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

def update_prices(request):
	old_data = {'titles':[], 'prices':[]}
	new_data={'titles':[], 'prices':[]}
	manager = request.user.is_manager
	user = request.user.full_name
	if manager:
		user_store = request.user.store_name
		store = Store.objects.get(title=user_store)
		prods = Product.objects.filter(store=store)
		for p in prods:
			titles = p.title
			old_prices = p.price
			old_data['titles'].append(titles)
			old_data['prices'].append(old_prices)
		if request.POST:
			file = request.FILES['myfile']
			data = pd.read_excel(file)

			for price, title in zip(data['price'], data['title']):
				products = Product.objects.filter(store=store)
				product = products.get(title = title)
				new_data['titles'].append(product)
				new_data['prices'].append(price)
				product.price = price
				product.save()
				send_mail(f'Онлайн магазин - "Потный айтишник"', f'{store} Изменил цены на свои товары. Старое: {old_data}, новое:{new_data}',EMAIL_HOST_USER,
						  [EMAIL_HOST_USER,])

		context = {'text': 'text', 'user': user, 'user_store': user_store}

		return render(request, 'update_prices.html', context)
	else:
			store = 'Вы не закреплены ни за одним магазином осуществляющим продажу на платформе "Потный айтишник". Уходите...'
			context = {'text': 'text', 'user': user, 'user_store': store}
			return render(request, 'update_prices.html', context)

def make_unavailable(request):
	manager = request.user.is_manager
	user = request.user.full_name
	products =[]

	if manager:
		user_store = request.user.store_name
		store = Store.objects.get(title=user_store)
		prods = Product.objects.filter(store=store)
		print(prods)
		for product in prods:
			form = ProductForm(request.POST, instance=product)
			# print(form)

			if form.is_valid():

				form.save()
		context = {'text': 'text', 'user': user, 'user_store': store, 'products': prods}
		# context = {'text': 'text', 'user': user, 'user_store': store,'product':prods, 'form':form}

		return render(request, 'make_products_unavaliable.html', context)
	# else:
	# 	return redirect('shop:go_away')


# form = EditProfileForm(request.POST, instance=request.user)
# if form.is_valid():
# 	form.save()
# 	messages.success(request, 'Ваш профиль был изменен', 'success')
# 	return redirect('accounts:edit_profile')
# else:
# 	form = EditProfileForm(instance=request.user)
# context = {'title': 'Edit Profile', 'form': form}
# return render(request, 'edit_profile.html', context)