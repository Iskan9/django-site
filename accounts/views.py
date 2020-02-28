from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm # для создания формы регистрации

from .forms import OrderForm, CreateUserForm # импортируем форму, которую мы создали в forms
from .filter import OrderFilter # для фильтрации в поиске

from .models import * # импортируем наши модели

from django.contrib import messages # импортируем сообщение, которое должно появится после регистрации
from django.contrib.auth import authenticate, login, logout  # импортируем
# аутентификацию, вход в систему и выход из системы

from django.contrib.auth.decorators import login_required # импортируем декоратор
# который ограничивает доступ( далее не зарегистрированных пользователей)
# то есть без регистрации и вхождения в систему, посмотреть данные не удасться, поэтому
# мы перед каждой функцией, которая отображает нужный нам контент, ставим декоратор

from .decorators import *  # импортируем все наши декораторы

from django.contrib.auth.models import Group # импортируем Group
# Далее с помощью Group все новые польз., автоматически ассоциируются с существующей группой "Сторонний_пользователь"


@unauthenticated_user # применяем декоратор, при попытке вошедшего в систему пользователя, перейти к register/
def registerPage(request):
    """Регистрация пользователя"""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Сторонний_пользователь') # создаем объект Group
            user.groups.add(group)  # и добавили нового пользователя в эту группу

            Customer.objects.create( # добавляем нового пользователя в таблицу Customer
                #  и при вхождении в систему, пользователь увидит статистику, подобно другим пользователям,
                # только у него будет нулевая статистика
                user=user,
                name=user.username,
            )

            messages.success(request, 'Аккаунт ' + username + " успешно создан")
            return redirect('login')  # после успешной регистрации перенаправялем на login.html
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    """Логин"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # входим в систему
            return redirect('home')  # и перенаправляемся на домашнюю стр
        else:
            messages.info(request, 'Логин или пароль неверны')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    """Выйти из системы"""
    logout(request) # функция импортированная
    return redirect('login')  # возвращаем на страницу login


@login_required(login_url='login')
@allowed_users(allowed_roles=['Сторонний_пользователь']) # для стороннего пользователя
def userPage(request):
    """Функция для пользователя"""
    orders = request.user.customer.order_set.all()
    total_orders = orders.count() # всего заказов
    delivered = orders.filter(status='Доставлено').count() # заказы со статусом доставлено
    pending = orders.filter(status='В ожидании').count() # заказы со статусом в ожидании

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')  # просмотр разрешен, если пользователь зашел в систему
@admin_only # если группа Админ, отобразить декорируемую функцию, иначе отобразить user.html
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Админ']) # фнкционал только для админа
def products(request):
    products = Product.objects.all() # запросить из базы все продукты
    return render(request, 'accounts/products.html', {'products': products})
    # название ключа в словаре, может быть любым, мы по нему потом обращаемся в html доке

@login_required(login_url='login')
@allowed_users(allowed_roles=['Админ'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)  # запросить из базы клиента по id
    orders = customer.order_set.all()  # Возвращает все заказы, связанные с клиентом
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders) # создаем экзепляр класса из filter.py
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}  # чтобы можно было обращаться через html
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Админ'])
def createOrder(request, pk):
    """Функция для создания заказа
    order_form.html переход по стр происходит не через href, а через method POST"""
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})  # создаем экзмепляр нашего класса OrderForm()

    if request.method =='POST':  # если метод POST
        # form = OrderForm(request.POST)  # передаем форме  post данные
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid(): # если данные действительны или валидны
            formset.save() # сохраним форму ( вроде в базе данных)
            return redirect('/') # и перенаправим на домашнюю стр

    context = {'form': formset}  # далее мы по ключу передадим form  в order_form.html
    return render(request, 'accounts/order_form.html', context)  # возвращаем order_form.html


@login_required(login_url='login')
@allowed_users(allowed_roles=['Админ'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Админ'])
def deleteOrder(request, pk):
    """Удалить заказ"""
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/') # вернуть на домашнюю стр
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

