from django.contrib import admin


from .models import *  # импортируем все модели( классы )

#  регистрируем наши модели
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)

