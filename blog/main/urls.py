from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('show_post/<slug:post_slug>', views.ShowPost.as_view(), name='show_post'),
    path('show_category/<slug:category_slug>', views.ShowCategory.as_view(), name='show_category'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('my_account', views.MyAccount.as_view(), name='my_account'),
    # path('password', auth_views.PasswordChangeView.as_view(template_name='main/change-password.html'))
    path('password/', views.PasswordsChangeView.as_view(template_name='main/change_password.html')),
    path('password_success', views.password_success, name='password_success'),
]

