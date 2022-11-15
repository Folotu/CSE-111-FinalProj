from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from invent.models import Product, OrderItem
from .utils import cookieCart, cartData, guestOrder

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	qauntDict = {}
	testprod = Product.objects.using('Inventory_db').all()
	testorderitems = OrderItem.objects.using('Inventory_db').all()
	for rex in testprod:
		yeat = 0
		for leftorders in testorderitems:
			if (rex.id == leftorders.product_id):
				yeat = yeat + leftorders.quantity
		qauntDict[rex.id] = 150 - yeat
		
	products = Product.objects.using('Inventory_db').all()
	context = {'products':products, 'cartItems':cartItems, 'howmanyleft':qauntDict,}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.using('Inventory_db').get(id=productId)
	order, created = Order.objects.using('customer_db').get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.using('Inventory_db').get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save(using='customer_db')

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.using('customer_db').get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save(using='customer_db')

	if order.shipping == True:
		ShippingAddress.objects.using('customer_db').create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)