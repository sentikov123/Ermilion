from django.contrib.auth import get_user_model
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import reverse, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Post, Category
from .form import PostForm, LoginUserForm, RegisterUserForm, PasswordChangingForm

logger = logging.getLogger('main')


class PostIndex(ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        extra_user = {
            'username': self.request.user,
            'userip': self.request.META['REMOTE_ADDR'],
            'path': self.request.path,
        }
        logger.info('Getting posts from db', extra=extra_user)
        return PostIndex.model.objects.all().order_by('-publish_date', 'title').select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Главная'
        context['categories'] = Category.objects.all()
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    login_url = reverse_lazy('main:login')
    template_name = 'main/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать новый пост'
        return context


class ShowPost(DetailView):
    model = Post
    template_name = 'main/show_post.html'
    slug_url_kwarg = 'post_slug'


class ShowCategory(ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return ShowCategory.model.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        cat = Category.objects.get(slug=self.kwargs['category_slug'])
        context['title'] = f'Категория: {cat.name}'
        context['categories'] = Category.objects.all()
        context['selected_cat'] = cat.name
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse('main:index')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('main:index')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


# class PasswordAccepted(DetailView):
#     template_name = 'main/password_accepted.html'

def password_success(request):
    return render(request, 'main/password_success.html', {})


# PtHfNeK365963548

class MyAccount(LoginView):
    form_class = LoginUserForm
    template_name = 'main/my_account.html'
    # slug_url_kwarg = 'post_slug'
