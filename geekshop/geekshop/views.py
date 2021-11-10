from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product, Contacts

menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products:main', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
]


def main(request):
    title = 'Магазин'

    products = Product.objects.all()[:3]

    context = {
        'title': title,
        'menu_item': menu_item,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    contact_list = Contacts.objects.all()

    context = {
        'title': title,
        'menu_item': menu_item,
        'contact_list': contact_list,
    }
    return render(request, 'geekshop/contact.html', context)


def not_works_page(request):
    return render(request, 'geekshop/base.html')
