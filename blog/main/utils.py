from django.core.cache import cache

from .models import Category


class ContextMixin:
    def get_user_context(self, **kwargs) -> dict:
        context = kwargs

        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)

        context['cats'] = cats

        return context


class UserData:
    def get_user_data(self):
        user_data = {
            'username': self.request.user,
            'userip': self.request.META['REMOTE_ADDR'],
            'path': self.request.path,
            'POST': self.request.POST
        }
        if self.request.method == "POST":
            user_data['POST'] = self.request.POST

        return user_data

