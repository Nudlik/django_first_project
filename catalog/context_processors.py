def menu(request):
    menu_list = [
        {'title': 'Главная', 'url_name': 'catalog:home'},
        {'title': 'Магазин',
         'submenu': [
             {'title': 'Каталог', 'url_name': 'catalog:list_product'},
             {'title': 'Категории', 'url_name': 'catalog:list_category'},
             {'title': 'Добавить продукт', 'url_name': 'catalog:create_product'},
         ]},
        {'title': 'Статьи', 'submenu': [
            {'title': 'Все посты', 'url_name': 'blog:post_list'},
            {'title': 'Добавить пост', 'url_name': 'blog:post_create'},
        ]},
        {'title': 'Контакты', 'url_name': 'catalog:contacts'},
    ]
    return {'menu': menu_list}
