from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from unidecode import unidecode
from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import PermissionsMixin


class Category(models.Model):
    name = models.CharField('Имя', max_length=20, unique=True, db_index=True)
    slug = models.SlugField('URL', max_length=20, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = [['name', 'slug']]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Название', max_length=500)
    slug = models.SlugField('URL статьи', max_length=500, unique=True, db_index=True)
    text = models.TextField('Текст')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    image = models.ImageField('Картинка', upload_to='main')
    publish_date = models.DateTimeField('Время публикации', max_length=500, auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        get_latest_by = 'publish_date'

    def get_absolute_url(self):
        return reverse('main:show_post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        last_obj = Post.objects.all().order_by('id').last()
        if last_obj:
            last_pk = last_obj.pk + 1
        else:
            last_pk = 1
        string = unidecode(str(self.title) + str(last_pk))
        self.slug = slugify(string)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Почтовый адрес должен быть задан!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почтовый адрес', max_length=50, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.CharField('bio', max_length=100, blank=True)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    @classmethod
    def get_username_by_id(cls, id):
        user = cls.objects.get(pk=id)
        username = user.email.split('@')[0]
        return username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

