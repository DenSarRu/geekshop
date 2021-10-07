import json

from django.shortcuts import render

menu_item = [
    {'href': 'main', 'name': 'домой'},
    {'href': 'products', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
    {'href': 'not_works_page', 'name': 'it is not work'},
]


def products(request):
    title = 'Каталог'
    links_menu = [
        {'href': 'products', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
        {'href': 'products_classic_not_dead', 'name': 'нетленка'},
    ]

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_item': menu_item,
    }
    return render(request, 'mainapp/products.html', context)
