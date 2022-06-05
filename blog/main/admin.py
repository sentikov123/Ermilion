# регистрация модели проекта в админ панели
from django.contrib import admin

from .models import Post, Category, User


class PostAdmin(admin.ModelAdmin):
    # выбор полей для отображения
    list_display = ('id', 'title', 'slug', 'image', 'publish_date')
    # выбор ссылок на пост
    list_display_links = ('id', 'title')
    # по каким полям осуществлять поиск
    search_fields = ('title', 'text')
    # сортировка по дате
    list_filter = ('publish_date',)
    # уникальная строка идентифифкатор
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
