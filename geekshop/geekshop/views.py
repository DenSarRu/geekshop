from django.shortcuts import render

from mainapp.models import Product, Contacts


def main(request):
    title = 'Магазин'
    print('all')

    products = Product.objects.all()[:3]

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context)


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
