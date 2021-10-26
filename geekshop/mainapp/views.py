from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
import random


menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products:main', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
]


def basket_check(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    return basket


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_product(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    title = 'Каталог'

    products_list = Product.objects.all().order_by('price')
    product_category_list = ProductCategory.objects.all()

    for item in ProductCategory.objects.all():
        if not products_list.filter(category=item).exists():
            cat = product_category_list.filter(name=item)[0]
            cat.is_active = False
            cat.save()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category = {'name': 'Все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')
            print(products_list)

        context = {
            'title': title,
            'menu_item': menu_item,
            'product_category_list': product_category_list,
            'category': category,
            'products_list': products_list,
            'basket': basket_check(request),
        }
        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'menu_item': menu_item,
        'product_category_list': product_category_list,
        'products_list': products_list,
        'same_products': same_products,
        'hot_product': hot_product,
        'basket': basket_check(request),
    }

    return render(request, 'mainapp/products.html', context)


# def category(request, pk=None):
#     print(pk)
#     return render(request, 'mainapp/products.html')


def product(request, pk):
    title = 'Описание товара'

    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'menu_item': menu_item,
        'product_category_list': ProductCategory.objects.all(),
        'product': product,
        'same_products': get_same_product(product),
        'basket': basket_check(request)
    }
    return render(request, 'mainapp/product.html', context)
