from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import redirect
from django.contrib import messages

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
		
	products = Product.objects.using('default').all()
	context = {'products':products, 'cartItems':cartItems, 'howmanyleft':qDict,}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	total = data['total']

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'total':total}
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	total = data['total']
	context = {'items':items, 'order':order, 'cartItems':cartItems, 'total': total}
	return render(request, 'store/checkout.html', context)

"""
Updates stock of a product after a purchase is made
:param quantity: a map of products being purchased and the quantity of the products purchased
"""
def updateStock(quantity):
	for id in quantity:
		p = Product.objects.get(id=id)
		p.stock = p.stock - quantity[id]
		p.save()

"""
Drops temp user and customer from database after a guest order is filled
:param customer: The customer (Customer db model) to delete from database. Customer also contains the user to delete.
"""
def drop_temp_user(customer):
	tCustomer = Customer.objects.get(CustomerID=customer.CustomerID)
	tUser = tCustomer.user
	instance = tCustomer
	instance.delete()
	instance = tUser
	instance.delete()

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
	# actually returns cart total (inefficient implementation)
	order_data = cartData(request)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.using('default').get_or_create(customer=customer, complete=False)
	else:
		customer, order, total, quantity = guestOrder(request, data)

	# total = float(data['form']['total'])
	order.transaction_id = transaction_id

	# if total == order.get_cart_total:
	if total == order_data['order']['get_cart_total']:
	# if total == order.get_cart_total:
		order.complete = True
	order.save(using='default')
	
	if order.complete:
		updateStock(quantity)
		drop_temp_user(customer)

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
		if request.user.is_authenticated:
			try:
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
			except:
				messages.error(request, "You are not a Seller!!")
				return redirect('/')
		else:
			return redirect('/login')

	if request.method == 'POST':
		
		products = Product.objects.using('default').all()

		print(request.POST['EVENT'])
		if request.POST['EVENT'] == "remove":
			req = request.POST
			prodID = req['whatProdIDtoRem']
			sellerID = req['whatSellerProdRem']

			Product.objects.filter(ProductID = prodID, sellerid = sellerID).delete()

			return redirect('/seller')

		if request.POST['EVENT'] == "edit":
			reqedit = request.POST
			prodname = reqedit['name']
			prodprice = reqedit['price']

			try:
				prodimage = request.FILES['image']
			except:
				prodim = Product.objects.filter(name=prodname).all()
				for j in prodim:
					prodimage = j.image

			try: 
				prodDigi = reqedit['digital']

			except:
				messages.error(request, "Unable to update item, you might have forgot to set digital option")
				return redirect('/seller')

			if prodDigi == 'Yes':
				prodDigi = True
			else:
				prodDigi = False

			prodStock = reqedit['stock']

			prodID = reqedit['whatProdIDtoRem']
			sellerID = reqedit['whatSellerProdRem']

			try:
				ProdSpecSeller = Product.objects.filter(ProductID = prodID, 
													sellerid = sellerID).update(
													name =  prodname, 
													price = prodprice,
													image = prodimage,  
													digital = prodDigi, 
													stock = prodStock)
	

			except:
				messages.error(request, "Unable to update item")

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

			try:
				newProdimage = request.FILES['image']
			except:
				newProdim = Product.objects.filter(name=newProdname).all()
				for j in newProdim:
					newProdimage = j.image

			newProdDigi = newProd['digital']

			if newProdDigi == 'Yes':
				newProdDigi = True
			else:
				newProdDigi = False

			newProdStock = newProd['stock']
			
			try:
				newProdSpecSeller = Product.objects.create(sellerid = request.user.seller, 
										ProductID = newProdIDtobe,
										name = newProdname, price = newProdprice, 
										image = newProdimage, digital = newProdDigi,
										stock = newProdStock)
			except:
				messages.error(request, "You already sell this Item")
				return redirect('seller')

			newProdSpecSeller.save()

			return redirect('/seller')

		return redirect('/seller')




