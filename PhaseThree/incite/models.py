from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	id = models.AutoField(primary_key=True)
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	Firstname = models.CharField(max_length=200, null=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyAccountManager()

	def __str__(self):
		return self.email + f", {self.Firstname}" 

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True



class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	CustomerID = models.AutoField(primary_key=True)
	#name = models.CharField(max_length=200, null=True)
	# email = models.EmailField(max_length=200, unique=True)
	# password = models.CharField(max_length=50, null=False)
	
	ship_addr = models.CharField(max_length=200, null=False, blank=True)
	bill_addr = models.CharField(max_length=200, null=False, blank=True)

	def __str__(self):
		return self.user.Firstname

class Seller(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	#SellerID = models.AutoField(User, blank=False, on_delete=models.CASCADE, primary_key=True)
	SellerID = models.AutoField(primary_key=True)
	#SellerID_id = models.IntegerField(primary_key=True)
	#email = models.EmailField(max_length=200, unique=True)
	#name = models.CharField(max_length=200, null=True)
	# password = models.CharField(max_length=50, null=False)
	# productid = models.IntegerField(default=False,null=True, blank=True)

	#productid = models.ManyToManyField('Product', default=False,null=True, blank=True,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.Firstname


class Product(models.Model):
	#id = models.OneToOneField(Seller.productid, null=True, blank=False, on_delete=models.CASCADE )
	# sellerid = models.ForeignKey(Seller.id, on_delete=models.SET_NULL, null=True)
	id = models.AutoField(primary_key=True)
	ProductID = models.IntegerField()
	sellerid = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200)
	price = models.FloatField()
	image = models.ImageField(null=True, blank=True)
	digital = models.BooleanField(default=False,null=True, blank=True)
	stock = models.IntegerField()

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['ProductID', 'sellerid'], name='uniqueProductSellerCombo'
            )
        ]
	
	def __str__(self):
		return self.name + f" Sold by {self.sellerid.user.Firstname}"

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	OrderID = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	Order_Date = models.DateTimeField(auto_now_add=True)
	Receipt_Date = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.IntegerField( null=True)

	def __str__(self):
		return f'Order Number {str(self.OrderID)}'
		
	@property
	def shipping(self):
		shipping = False
		orderitems = Order_item.objects.using('default').filter(order=self.OrderID).all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping



class Order_item(models.Model):
	OrderItemID = models.AutoField(primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	def __str__(self):
		return f'{self.product.name} from {self.product.sellerid}: ({str(self.order)})'


class Cart(models.Model):
	# CustomerID = models.ForeignKey(Customer.id, on_delete=models.SET_NULL, null=True)
	CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE,  blank= True, null=True)
	# OrderID = models.ForeignKey(Order.id, on_delete=models.SET_NULL, null=True )

	#SpecificOrders = Order.objects.get(customer = CustomerID)

	OrderID = models.ForeignKey(Order, on_delete=models.CASCADE,  blank= True, null=True )

	CartID = models.AutoField(primary_key=True)

	# @property
	# def __init__(self, *args, **kwargs):
	# 	super(Cart, self).__init__(*args, **kwargs)
	# 	self.fields['description'].widget.attrs={
    #         'id': 'CartID',
    #         }
	
	# Cart_total = orderitems = orderitem_set.all()
	# total = sum([item.get_total for item in orderitems])

	@property
	def get_cart_total(self):
		# orderitems = self.orderitem_set.all()
		orderitems = Order_item.objects.using('default').filter(order=self.OrderID).all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		# orderitems = self.order_item_set.all()
		orderitems = Order_item.objects.using('default').filter(order=self.OrderID).all()
		total = sum([item.quantity for item in orderitems])
		return total 



class Checkout(models.Model):
	CheckoutID = models.AutoField(primary_key=True)
	# CustomerID = models.ForeignKey(Customer.id, on_delete=models.SET_NULL, null=True)
	# CustomerID = models.ForeignKey(Customer.id, on_delete=Customer.SET_NULL, null=True)
	CustomerID = models.ForeignKey(Customer, blank= True, on_delete=models.CASCADE, null=True)
	# CartID = models.ForeignKey(Cart.id, on_delete=models.SET_NULL, null=True )
	CartID = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True )
	# SellerID = models.ForeignKey(Seller.id, on_delete=models.SET_NULL, null=True )
	SellerID = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True )

