# ***(1)Возвращает всех клиентов из таблицы клиентов
# customers = Customer.objects.all()

# (2)Возвращает первого клиента в таблице
# firstCustomer = Customer.objects.first()

# (3)Возвращает последнего клиента в таблице
# lastCustomer = Customer.objects.last()

# (4)Возвращает одного клиента по имени
# customerByName = Customer.objects.get(name='Peter Piper')

# ***(5)Возвращает одного клиента по имени
# customerById = Customer.objects.get(id=4)

# ***(6)Возвращает все заказы, связанные с клиентом (переменная firstCustomer, указанная выше)
# firstCustomer.order_set.all()

# (7)***Возвращает заказчику имя клиента: (запрос значений родительской модели)
# order = Order.objects.first()
# parentName = order.customer.name

# (8)***Возвращает товары из таблицы товаров со значением "Out Door" в атрибуте категории
# products = Product.objects.filter(category="Out Door")

# (9)***Упорядочить / Сортировать объекты по идентификатору
# leastToGreatest = Product.objects.all().order_by('id')
# greatestToLeast = Product.objects.all().order_by('-id')


# (10) Returns all products with tag of "Sports": (Query Many to Many Fields)
# productsFiltered = Product.objects.filter(tags__name="Sports")

'''
(11)Bonus
Q: Если у клиента более 1 шара, как бы вы отразили его в базе данных?
A: Так как есть много разных продуктов, и это их количество или наименование  меняется, мы
скорее всего хотели бы  не хранить значение в базе данных, а просто сделать это функцией, которую мы можем запустить
каждый раз, когда мы загружаем профиль клиента
'''

# Возвращает общее количество за время, в течение которого «Шарик» был заказан первым клиентом.
# ballOrders = firstCustomer.order_set.filter(product__name="Ball").count()

# Возвращает общее количество для каждого заказанного товара
# allOrders = {}
"""
for order in firstCustomer.order_set.all():
	if order.product.name in allOrders:
		allOrders[order.product.name] += 1
	else:
		allOrders[order.product.name] = 1

#Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}


#RELATED SET EXAMPLE
class ParentModel(models.Model):
	name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
	parent = models.ForeignKey(Customer)
	name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
#Возвращает все дочерние модели, связанные с родителем
parent.childmodel_set.all()

"""