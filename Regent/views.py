
from typing import Text
from django import http
from django.contrib import auth
from django.db.models.fields import DateField
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
import base64
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, JsonResponse, FileResponse, response
from django.core.files import File
import json
from django.urls import reverse


# Create your views here.

@login_required(login_url="/login/")
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
@login_required
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

@login_required
def checkout(request):       
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else: 
        items = []
        order = {"get_cart_item":0,"get_cart_total":0}
        cartItem = order['get_cart_item']
    context = {"items":items,"order":order,'cartItem':cartItem}
    return render(request,"checkout.html",context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
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

def processOrder(request):
    global data
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,orderstatus=False)
        global order_id
        order_id= order.ordercode
        total= float(data['form']['total'])
        if total == order.get_cart_total:
            order.orderstatus=True
        order.save()
        if order.orderstatus is True:
            CustomerDetails.objects.create(
                name=customer,
                order=order,
                phone=int(data['form']['phone']),
                ordertype=data['form']['ordertype'],
                table=int(data['form']['tableno']),
                time=data['form']['time'],
            )
    else:
        print("The user is not logged in")
    return JsonResponse('payment is complete',safe=False)

def order_receipt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']= 'attachment; filename=Receipt.txt'
    if request.user.is_authenticated:
        customer = request.user.profile
        cust_details = CustomerDetails.objects.all().filter(name=customer)[::-1]
        lines=[]
        for details in cust_details:
            lines.append(f"Name: {details.name}\n Order no: {details.order}\n phone no:{details.phone}\n Order Type:{details.ordertype}\n Table no:{details.table}\n Time:{details.time}\n\n *****End*****\n")
        response.writelines(lines)
        return response
        






#the mpesa function 
def transaction(request):
    cl = MpesaClient()
    phone_number = str(data['form']['phone']) #data['form']['phone']#customer phone number # Use a Safaricom phone number that you have access to, for you to beable to view the prompt.
    amount = int(data['form']['total'])#total
    account_reference = 'Messtech'
    transaction_desc = 'your order {order_id }'
    callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference,transaction_desc, callback_url)
    return HttpResponse(response.text)

@login_required
def stk_push_callback(request):
    Mpesa_messages = request.body#mpesa message
    with open("transactions",mode="a",encoding="utf-8") as f:
        f = File(f)
        f.write(Mpesa_messages)
   



def Login(request):
    if request.method == "POST":
        UserName = request.POST['Uname']
        password1 = request.POST['Password1']
        print(password1)
        user = auth.authenticate(request,username=UserName,password=password1)
        if user is not None:
            auth.login(request,user)
            print(user)
            return redirect("/")
        else:
            messages.info(request,"invalid credentials")
            return redirect("login")
    else:
        
        return render(request,"login.html")

def signup(request):
    if request.method == "POST":
        FirstName = request.POST['Fname']
        LastName = request.POST['Lname']
        UserName = request.POST['Uname']
        Email = request.POST['Email']
        password1 = request.POST['Password1']
        password2 = request.POST['Password2']
        if password1 == password2:
            if User.objects.filter(username=UserName).exists():
                messages.info(request,"username already exist, try another username")
            elif User.objects.filter(email=Email):
                messages.info(request,"email already in use")
            else:
                user=User.objects.create(username=UserName,email=Email,password=password1,first_name=FirstName,last_name=LastName,is_active=True,is_superuser=False,is_staff=False)
                messages.success(request,"account created succesfully proceed to login",fail_silently=True)
                user.save()
                
            return redirect("login")
                
        else:
            messages.info(request,"incorrect password")
         
    else:
        return render(request,"signup.html")

def logout_view(request):
    auth.logout(request)
    return render(request,"logout.html")

@staff_member_required
def dashboard(request):
    if request.user.is_authenticated:
        total_customer = Profile.objects.all().count()
        order_items = OrderItem.objects.all()[::-1]
        completed_orders = Order.objects.filter(orderstatus=True).count()
        all_customer_details = CustomerDetails.objects.all()[::-1]
        context={
            "completed_orders":completed_orders,
            "order_items":order_items,
            "total_customer":total_customer,
            "all_customer_details":all_customer_details
        }
    return render(request,"dashboard.html",context)

