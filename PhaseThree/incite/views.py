from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	qDict = {}
	testprod = Product.objects.using('default').all()
	# Get live stock from DB
	for p in testprod:
		qDict[p.id] = p.stock
	testorderitems = Order_item.objects.using('default').all()
	"""
	TODO - Move this commented block to checkout so stock gets updated
	"""
	# for rex in testprod:
	# 	yeat = 0
	# 	for leftorders in testorderitems:
	# 		if (rex.id == leftorders.product_id):
	# 			yeat = yeat + leftorders.quantity
	# 	qDict[rex.id] = qDict[rex.id] - yeat
		
	products = Product.objects.using('default').all()
	context = {'products':products, 'cartItems':cartItems, 'howmanyleft':qDict,}
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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def updateItem(request):
	print(request)
	print(request.GET)
	try:
		data = json.loads(request.body)
		productId = data['productId']
		action = data['action']
		print('Action:', action)
		print('Product:', productId)
		
		customer = request.user.customer
		product = Product.objects.using('default').get(id=productId)
		order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)

		orderItem, created = Order_item.objects.using('default').get_or_create(order=order, product=product)

		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)

		elif action == 'remove':
			orderItem.quantity = (orderItem.quantity - 1)
			
		orderItem.save(using='default')
		
		if orderItem.quantity <= 0:
			orderItem.delete()

	except: 

		customer = request.user.customer
		order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)

		order_items = Order_item.objects.using('default').filter(order = order).all()
		print(order_items)
		items = []
		{'get_cart_total': len(order_items), 'get_cart_items':0, 'shipping':False}
		for j in order_items:
			print(j.product)
			items.append(j.product)


	return JsonResponse('Item was added', safe=False)




@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	# if total == order.get_cart_total:
	if total == order.get_cart_total:
		order.complete = True
	order.save(using='default')

	# if order.shipping == True:
	# 	ShippingAddress.objects.using('default').create(
	# 	customer=customer,
	# 	order=order,
	# 	address=data['shipping']['address'],
	# 	city=data['shipping']['city'],
	# 	state=data['shipping']['state'],
	# 	zipcode=data['shipping']['zipcode'],
	# 	)

	return JsonResponse('Payment submitted..', safe=False)
