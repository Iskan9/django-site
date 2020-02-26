from django.forms import ModelForm
from .models import Order  # импортируем модель Order

class OrderForm(ModelForm):
    class Meta:
        model = Order  # указываем форму какой модели мы хотим создать
        fields = '__all__'  # "наследуем" все поля(атрибуты класса Order)

