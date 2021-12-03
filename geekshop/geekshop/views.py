from django.shortcuts import render
from django.views.decorators.cache import cache_page

from mainapp.models import Product, Contacts


def main(request):
    title = 'Магазин'
    print('all')

    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    products = Product.get_items()[:3]

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context)


@cache_page(3600)
def contacts(request):
    title = 'Контакты'

    contact_list = Contacts.objects.all()

    context = {
        'title': title,
        'contact_list': contact_list,
    }
    return render(request, 'geekshop/contact.html', context)


def not_works_page(request):
    return render(request, 'geekshop/base.html')
