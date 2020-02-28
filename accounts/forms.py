from django.forms import ModelForm
from .models import * # импортируем все модели

from django.contrib.auth.forms import UserCreationForm # импортируем форму регистрации
from django.contrib.auth.models import User # еще ипортируем
from django import forms


class OrderForm(ModelForm):
    class Meta:
        model = Order  # указываем форму какой модели мы хотим создать
        fields = '__all__'  # "наследуем" все поля(атрибуты класса Order)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):  # добавил форму для "настройки аккаунта"
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user'] # исключить поле пользователь