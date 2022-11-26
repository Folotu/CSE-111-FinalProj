from django.urls import path

from . import views, auth

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('login/', auth.login_user, name="login"),
	path('sign_up/', auth.sign_up, name="sign_up"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]