from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Create your models here.


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'inputLogin',
                                                             'autofocus': 'autofocus'}))
    password = forms.CharField(label='Пароль',
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'id': 'inputPassword'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин*',
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'inputLogin',
                                                             'autofocus': 'autofocus'}))
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'inputName'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id': 'inputSurname'}))
    email = forms.EmailField(label='Email*',
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'id': 'inputEmail'}))
    password1 = forms.CharField(label='Пароль*',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'inputPassword1'}))
    password2 = forms.CharField(label='Повтор пароля*',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'inputPassword2'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password1')
