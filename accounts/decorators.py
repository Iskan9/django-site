from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """Неаутентифицированный пользователь"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # если пользователь уже аутентифицирован
            # то есть он вошел в систему, но зачем-то попытался получить доступ к ../login/, то
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs) # иначе возвращаем декоририруемую функцию
    return wrapper_func


def allowed_users(allowed_roles=[]):
    """Разрешенные пользователи"""
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists(): # если группа сущесвует
                group = request.user.groups.all()[0].name # взять первый элемент из списка

            if group in allowed_roles: # если group есть среди разрешенных пользователей
                return view_func(request, *args, **kwargs) # возвращаем представление декорируемой функции
                # то есть возвращаем ту функцию, над которой мы написали этот декоратор
            else:
                return HttpResponse('Вы не авторизованы для просмотра данной страницы')
        return wrapper_func
    return decorator


def admin_only(view_func):
    """Только для группы: Админ"""
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Сторонний_пользователь':
            return redirect('user-page')

        if group == 'Админ':
            return view_func(request, *args, **kwargs)

    return wrapper_function