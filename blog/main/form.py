from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import ModelForm, TextInput, Textarea, FileInput, Select, PasswordInput, CharField, EmailInput

from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название статьи'
        self.fields['text'].label = 'Текст статьи'
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.label_suffix = ''

    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'category': Select(attrs={
                'class': 'form-select'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст статьи'
            }),
            'image': FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if '!' in title:
            self.add_error('title', 'Название не должно содержать восклицательных знаков!')
        if len(title) < 10:
            self.add_error('title', 'Слишком маленькое название статьи, должно быть больше 10 символов')
        return title


class LoginUserForm(AuthenticationForm):
    username = CharField(
        label='Почта',
        widget=EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта',
                'id': 'floatingInput'
        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'id': 'floatingPassword'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    email = CharField(
        label='Почта',
        widget=EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта',
                'id': 'floatingInput',
                'name': 'email'
        })
    )
    password1 = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'id': 'floatingPassword'
        })
    )
    password2 = CharField(
        label='Повторите пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'id': 'floatingPassword'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']


class PasswordChangingForm(PasswordChangeForm):
    old_password = CharField(
        label='Старый пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'type': 'password'
        })
    )

    new_password1 = CharField(
        label='Введите новый пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'type': 'password'
        })
    )

    new_password2 = CharField(
        label='Введите новый пароль ещё раз',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'type': 'password'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']