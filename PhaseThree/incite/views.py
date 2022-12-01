from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import redirect

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	qauntDict = {}
	testprod = Product.objects.using('default').all()
	testorderitems = Order_item.objects.using('default').all()
	for rex in testprod:
		yeat = 0
		for leftorders in testorderitems:
			if (rex.id == leftorders.product_id):
				yeat = yeat + leftorders.quantity
		qauntDict[rex.id] = 150 - yeat
		
	products = Product.objects.using('default').all()
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



@csrf_exempt
def sellerHome(request):

	if request.method == 'GET':
		products = Product.objects.using('default').all()

		uniqueProdName = []
		prodbb = []
		yourProds = []
		for i in range(len(products)):
			if products[i].name not in uniqueProdName:
				uniqueProdName.append(products[i].name)
				prodbb.append(products[i])

		for i in range(len(products)):
			if products[i].sellerid == request.user.seller:
				yourProds.append(products[i])


		context = {'products':prodbb, 'yourProds': yourProds}

		return render(request, 'store/seller.html', context)

	if request.method == 'POST':
		products = Product.objects.using('default').all()
		print(request.POST['EVENT'])
		if request.POST['EVENT'] == "remove":
			req = request.POST
			prodID = req['whatProdIDtoRem']
			sellerID = req['whatSellerProdRem']

			Product.objects.filter(ProductID = prodID, sellerid = sellerID).delete()

			return redirect('/seller')
		
		
		if request.POST['EVENT'] == "sell":

			newProd = request.POST
			for j in newProd:
				print(j)
			newProdname = newProd['name']
			

			maxID = 0
			for i in range(len(products)):
				maxID = max(products[i].ProductID, maxID)
				if products[i].name ==  newProdname:
					newProdIDtobe = products[i].ProductID
				else:
					newProdIDtobe = maxID +1

			newProdprice = newProd['price']

			newProdimage = ""

			if request.POST['fixIm'] == 0:
				newProdimage = request.FILES['image']
			else:
				newProdim = Product.objects.filter(name=newProdname).all()
				for j in newProdim:
					newProdimage = j.image

			newProdDigi = newProd['digital']

			if newProdDigi == 'Yes':
				newProdDigi = True
			else:
				newProdDigi = False

			newProdStock = newProd['stock']

			# newProdSpecSeller = Product(sellerid = request.user.seller, 
			# 							ProductID = newProdIDtobe,
			# 							name = newProdname, price = newProdprice, 
			# 							image = newProdimage, digital = newProdDigi,
			# 							stock = newProdStock)


			newProdSpecSeller = Product.objects.create(sellerid = request.user.seller, 
										ProductID = newProdIDtobe,
										name = newProdname, price = newProdprice, 
										image = newProdimage, digital = newProdDigi,
										stock = newProdStock)

			newProdSpecSeller.save()

			return redirect('/seller')



