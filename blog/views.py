from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from blog.utils import MenuMixin


class PostListView(MenuMixin, ListView):
    model = Post
    page_title = 'Список статей'
    page_description = 'Здесь можно посмотреть все статьи'
    paginate_by = 3

    def get_queryset(self):
        return self.model.published.all()


class PostDetailView(MenuMixin, DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()
        return obj


class PostCreateView(MenuMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    page_title = 'Страница для создания статьи'


class PostUpdateView(MenuMixin, UpdateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    page_title = 'Страница для редактирования статьи'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug'])


class PostDeleteView(MenuMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    page_title = 'Страницы для удаление статьи'
