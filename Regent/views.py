
from django import http
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from Regent.forms import CustomerForm
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files import File
import json
from django.urls import reverse
# Create your views here.
def index(request):
    meals = Meal.objects.all()[:10]
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items":0,"get_cart_total":0}
        cartItem = order['get_cart_items']
    context = {"items":items,"order":order,"cartItem":cartItem,"meals":meals}
    return render(request,"index.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        
        order = {"get_cart_items":0,"get_cart_total":0}
        cartItem = order['get_cart_items']
    context = {"items":items,"order":order,"cartItem":cartItem}
    return render(request,"cart.html",context)





    

def checkout(request):       
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
        items = order.orderitem_set.all()
        form = CustomerForm()
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                messages.success(request,"completed")
                form.save()
                return redirect('transaction')#you can give an emplty form
    else:
        form = CustomerForm()
        items = []
        order = {"get_cart_item":0,"get_cart_total":0}
    context = {"items":items,"order":order,"form":form}
    return render(request,"checkout.html",context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action',action)
    print('productId',productId)

    customer = request.user.profile
    product = Meal.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,products=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
        
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)



def Login(request):
    if request.method == "POST":
        UserName = request.POST['Uname']
        password1 = request.POST['Password1']
        user = authenticate(request,username=UserName,password=password1)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"invalid user try again or sign-up")
            return redirect("login")  
    return render(request,"login.html")

def signup(request):
    if request.method == "POST":
        FirstName = request.POST['Fname']
        LastName = request.POST['Lname']
        UserName = request.POST['Uname']
        Email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=UserName).exists():
                messages.info(request,"username already exist, try another username")
            elif User.objects.filter(email=Email):
                messages.info(request,"email already in use")
            else:
                user=User.objects.create(username=UserName,email=Email,password=password1,first_name=FirstName,last_name=LastName)
                user.save()
                messages.success(request,"user created succesfully",fail_silently=True)
                return redirect("login")
        else:
            messages.info(request,"incorrect password")
         
    else:
        return render(request,"signup.html")

def logout(request):
    logout(request)
    return render(request,"/")



#the mpesa function 
def transaction(request):
    cl = MpesaClient()
# Use a Safaricom phone number that you have access to, for you to beable to view the prompt.
    phone_number = '0757164343'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference,transaction_desc, callback_url)
    return HttpResponse(response.text)

def stk_push_callback(request):
    data = request.body
    with open("transactions",mode="a",encoding="utf-8") as f:
        f = File(f)
        f.write(data)
    return FileResponse(as_attachment=True,filename="f")
    


def dashboard(request):
    return render(request,"dashboard.html")

