def menu_item(request):
    # print('context_processor "menu" works!')

    context_menu_item = [
        {'href': 'main', 'name': 'домой'},
        {'href': 'products:main', 'name': 'продукты'},
        {'href': 'contacts', 'name': 'контакты'},
        # {'href': 'orders:main', 'name': 'Заказы'},

    ]

    return {
        'menu_item': context_menu_item,
    }
