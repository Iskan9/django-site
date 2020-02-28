from django.forms import ModelForm
from .models import Order  # импортируем модель Order

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