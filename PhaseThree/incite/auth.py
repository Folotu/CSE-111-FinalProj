from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cartData, guestOrder
from .utils import cartData
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import redirect
from .views import sellerHome

def login_user(request):
    
    if request.method == 'POST':
        context_instance = RequestContext(request)
        print(request)
        print(request)
        loginData = request.POST

        email = loginData['email']
        password = loginData['password']

        user = User.objects.filter(email=email).first()
        if user:

            # print(user.check_password(password))
            #check_password(user.password, password)
            print(user.password)
            print(password)
            if user.password == password:
                messages.success(request, 'Logged in successfully!')

                login(request, user)
                try: 
                    if user.seller:
                        return redirect('/seller')
                except:
                    if user.customer:
                        return redirect('/')

            else:
                messages.error(request, 'Incorrect password, try again.')
        else:
            messages.error(request, 'Email does not exist.')

    # elif request.method == 'GET':
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'store/login.html', context)


def logout_user(request):

    if request.user.is_authenticated:
        messages.success(request, 'Logged out successfully!')
        logout(request)
        return redirect('/login')
    else:
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'items':items, 'order':order, 'cartItems':cartItems}

        messages.success(request, 'You were never logged in!')
        return redirect(request, 'store/login.html', context)
    

def sign_up(request):

    if request.method == 'POST':
        context_instance = RequestContext(request)
        signUpdata = request.POST

        firstname = signUpdata['firstName']
        email = signUpdata['email']
        username = signUpdata['Username']
        password1 = signUpdata['password1']
        password2 = signUpdata['password2']
        CustomerOrSeller = signUpdata['theirRole']

        user = User.objects.filter(email=email)
        if user:
            messages.error(request, 'Email already exists.')
            return redirect('/sign_up')
        elif len(email) < 4:
            messages.error(request, 'Email must be greater than 3 characters.')
            return redirect('/sign_up')
        elif len(username) < 2:
            messages.error(request, 'First name must be greater than 1 character.')
            return redirect('/sign_up')
        elif password1 != password2:
            messages.error(request, 'Passwords don\'t match.')
            return redirect('/sign_up')
        elif len(password1) < 7:
            messages.error(request,'Password must be at least 7 characters.')
            return redirect('/sign_up')
        else:
            new_user = User(email=email, username=username, Firstname = firstname, password = password1) #password=make_password(password1))
            new_user.save()

            if (CustomerOrSeller == 'Customer'):
                new_customer = Customer(user=new_user)
                new_customer.save()

            elif (CustomerOrSeller == 'Seller'):
                new_seller = Seller(user=new_user)
                new_seller.save()
                login(request, new_user)
                messages.success(request, 'Account created!')
                return redirect('/seller')


            login(request, new_user)
            messages.success(request, 'Account created!')
            return redirect('/')

    elif request.method == 'GET':
        data = cartData(request) 
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items':items, 'order':order, 'cartItems':cartItems}

        return render(request, 'store/sign_up.html', context)
    
