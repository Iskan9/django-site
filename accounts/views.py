from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import OrderForm # импортируем форму, которую мы создали в forms

from .models import * # импортируем наши модели


def home(request):
    orders = Order.objects.all() # запросить из базы все заказы
    customers = Customer.objects.all()  # запросить из базы всех клиентов

    total_customers = customers.count()  # количестов всех клиентов
    total_orders = orders.count()  # количестов всех заказов
    delivered = orders.filter(status='Доставлено').count()
    pending = orders.filter(status='В ожидании').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all() # запросить из базы все продукты
    return render(request, 'accounts/products.html', {'products': products})
    # название ключа в словаре, может быть любым, мы по нему потом обращаемся в html доке


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)  # запросить из базы клиента по id
    orders = customer.order_set.all()  # Возвращает все заказы, связанные с клиентом
    order_count = orders.count()

    context = {'customer': customer, 'orders': orders, 'order_count': order_count} # чтобы можно было обращаться через html
    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    """Функция для создания заказа
    order_form.html переход по стр происходит не через href, а через method POST"""
    form = OrderForm()  # создаем экзмепляр нашего класса OrderForm()

    if request.method =='POST':  # если метод POST
        form = OrderForm(request.POST)  # передаем форме  post данные
        if form.is_valid(): # если данные действительны или валидны
            form.save() # сохраним форму ( вроде в базе данных)
            return redirect('/') # и перенаправим на домашнюю стр

    context = {'form': form}  # далее мы по ключу передадим form  в order_form.html
    return render(request, 'accounts/order_form.html', context)  # возвращаем order_form.html


def updateOrder(request, pk):
    """Обновить заказ"""
    order = Order.objects.get(id=pk) # запросить из базы клиента по id
    form = OrderForm(instance=order)  # создаем экземпляр нашего класса
    #  instance =  это экземпляр класса,  а в OrderForm передаем экзепляр класса
    # это значит, что при нажатии "обновить заказ"  в форме будут отображаться данные конкретного экземпляра

    if request.method == 'POST':  # если метод POST
        form = OrderForm(request.POST, instance=order)  # передаем форме  post данные и конкртеного экземпляра
        if form.is_valid(): # если данные действительны или валидны
            form.save() # сохраним форму   в базу данных
            return redirect('/') # и перенаправим на домашнюю стр

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)  # возвращаем order_form.html


def deleteOrder(request, pk):
    """Удалить заказ"""
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/') # вернуть на домашнюю стр
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

