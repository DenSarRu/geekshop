from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from random import randint

menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products:main', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
    #{'href': 'not_works_page', 'name': 'страница не работает'},#
]


def products(request, pk=None):
    title = 'Каталог'

    products_list = Product.objects.all()[1:randint(0, len(Product.objects.all()))]

    product_category_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'menu_item': menu_item,
        'product_category_list': product_category_list,
        'products_list': products_list,
    }
    print(pk)
    return render(request, 'mainapp/products.html', context)


def category(request, pk=None):
    print(pk)
    return render(request, 'mainapp/products.html')
