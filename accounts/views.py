from django.shortcuts import render
from django.http import HttpResponse


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
    customer = Customer.objects.get(id=pk_test)  # запросить из баз клиента по id
    orders = customer.order_set.all()  # Возвращает все заказы, связанные с клиентом
    order_count = orders.count()

    context = {'customer': customer, 'orders': orders, 'order_count': order_count} # чтобы можно было обращаться через html
    return render(request, 'accounts/customer.html', context)