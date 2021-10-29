from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def cart(request):
    return render(request,"cart.html")

def checkout(request):
    return render(request,"checkout.html")

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def dashboard(request):
    return render(request,"dashboard.html")
