from django.contrib import admin

from .models import Post, Category, User


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'image', 'publish_date')
    list_display_links = ('id', 'title')
    # list_editable = ('slug',)
    search_fields = ('title', 'text')
    list_filter = ('publish_date',)
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
