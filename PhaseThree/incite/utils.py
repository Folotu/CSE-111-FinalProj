import json
import uuid
from .models import *

num_temp_users = 0

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.using('default').get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{
					'id':product.id,
					'name':product.name, 
					'price':product.price, 
				        'imageURL':product.imageURL
					}, 
				'quantity':cart[i]['quantity'],
				'digital':product.digital,
				'get_total':total,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		# from .views import updateItem
		# updateItem(request)

		order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)
		items = Order_item.objects.using('default').filter(order = order).all()
		carti= Cart.objects.using('default').filter(CustomerID = customer, OrderID = order).all()
		print(carti)
		print(Cart.objects.using('default').filter(CustomerID = customer, OrderID = order))
		
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		for j in carti:

			cartItems = j.get_cart_items


		return {'cartItems':cartItems ,'order':order, 'items':items}
		# order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)

		# order_items = Order_item.objects.using('default').filter(order = order).all()
		# print(order_items)
		# items = []
		# {'get_cart_total': len(order_items), 'get_cart_items':0, 'shipping':False}
		# for j in order_items:
		# 	print(j.product)
		# 	items.append(j.product)

		# print(order)
	

		# items = order.orderitem_set.all()
		# print(order.OrderID)
		# print(items)
		# #orderItem, created = Order_item.objects.using('default').get_or_create(order=order, product=product)
		# cartItems = order.get_cart_items()
		# print(order)
		# # orderItems = 
		# print(order.orderitem)
		
		
		# print(items)
		
		# cartItems = order.get_cart_items()
		
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

		return {'cartItems':cartItems ,'order':order, 'items':items}

	

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']
	print(f"sugar {items}")
	user = User.objects.using('default').get_or_create(email=email, username=f"temp_user_{uuid.uuid4()}", password="abcd1234")
	actual_user = User.objects.using('default').get(email=email)
	customer, created = Customer.objects.using('default').get_or_create(
			user=actual_user
			)
	customer.name = name
	customer.email = email
	customer.save()
	
	order = Order.objects.using('default').create(
		customer=customer,
		complete=False,
		)
	total = 0
	for item in items:
		product = Product.objects.using('default').get(id=item['id'])
		orderItem = Order_item.objects.using('default').create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
		total += (item["product"]["price"]) * (item["quantity"])
	return customer, order, total

