from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product, Contacts

menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products:main', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
    # {'href': 'not_works_page', 'name': 'страница не работает'},#
]


def basket_check(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    return basket


def main(request):
    title = 'Магазин'

    products = Product.objects.all()[:3]

    context = {
        'title': title,
        'menu_item': menu_item,
        'products': products,
        'basket': basket_check(request),
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    contact_list = Contacts.objects.all()

    context = {
        'title': title,
        'menu_item': menu_item,
        'contact_list': contact_list,
        'basket': basket_check(request),
    }
    return render(request, 'geekshop/contact.html', context)


def not_works_page(request):
    return render(request, 'geekshop/base.html')
