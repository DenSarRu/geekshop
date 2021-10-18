from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


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


def products(request, pk=None):
    title = 'Каталог'

    products_list = Product.objects.all().order_by('price')
    product_category_list = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category = {'name': 'Все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')

        same_products = Product.objects.filter(category__pk=pk)[:3]

        context = {
            'title': title,
            'menu_item': menu_item,
            'product_category_list': product_category_list,
            'category': category,
            'products_list': products_list,
            'same_products': same_products,
            'basket': basket_check(request),
        }
        return render(request, 'mainapp/products.html', context)

    same_products = Product.objects.all()[1:3]

    context = {
        'title': title,
        'menu_item': menu_item,
        'product_category_list': product_category_list,
        'products_list': products_list,
        'same_products': same_products,
        'basket': basket_check(request),
    }

    return render(request, 'mainapp/products.html', context)


def category(request, pk=None):
    print(pk)
    return render(request, 'mainapp/products.html')
