from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from shop.models import Product, Category, Store, Characteristic, ProductCharacteristic
from cart.forms import QuantityForm


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
		'products': products
	}
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

