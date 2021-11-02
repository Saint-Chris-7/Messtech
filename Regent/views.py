
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required()
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitem_set.all()
    items = []
    order = {"get_cart_item":0,"get_cart_total":0}
    context = {"items":items,"order":order}
    return render(request,"cart.html",context)
    

def checkout(request):
    if user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items":0,"get_cart_total":0}
    context = {"items":items,"order":order}
    return render(request,"checkout.html",context)

def login(request):
    if request.method == "POST":
        UserName = request.POST['Uname']
        password1 = request.POST['password1']

        user = authenticate(request,username=UserName,password=password1)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"invalid user")
            return redirect("login")  
    return render(request,"login.html")

def signup(request):
    if request.method == "POST":
        FirstName = request.POST['Uname']
        LastName = request.POST['Lname']
        UserName = request.POST['Uname']
        Email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=UserName).exist():
                messages.info(request,"username already exist, try another username")
            elif User.objects.filter(emai=Email):
                messages.info(request,"email already in use")
            else:
                User.objects.create(firstname=FirstName,lastname=LastName,email=Email,password=password1)
                User.save()
                messages.success(request,"user created succesfully",fail_silently=True)
        else:
            messages.info(request,"incorrect password")
            return redirect("signup")
    else:
        return render(request,"/")    
    return render(request,"signup.html")


def logout(request):
    logout(request)
    return render(request,"/")

def dashboard(request):
    return render(request,"dashboard.html")

def foods(request):
    return render(request,"foods.html")

def beaverages(request):
    return render(request,"beaverages.html")