menu = [
    {'title': 'Главная', 'url_name': 'catalog:home'},
    {'title': 'Все посты', 'url_name': 'blog:post_list'},
    {'title': 'Добавить пост', 'url_name': 'blog:post_create'},
]


class MenuMixin:
    page_title: str = None
    page_description: str = None

    def get_mixin_context(self, context: dict, **kwargs) -> dict:
        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.page_title is not None:
            context['title'] = self.page_title

        if self.page_description is not None:
            context['description'] = self.page_description

        if 'menu' not in context:
            context['menu'] = menu

        return context
