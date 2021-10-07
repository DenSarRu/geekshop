from django.shortcuts import render

menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
    {'href': 'not_works_page', 'name': 'страница не работает'},
]


def main(request):
    title = 'Магазин'
    context = {
        'title': title,
        'menu_item': menu_item,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'
    context = {
        'title': title,
        'menu_item': menu_item,
    }
    return render(request, 'geekshop/contact.html', context)


def not_works_page(request):
    return render(request, 'geekshop/base.html')
