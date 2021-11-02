from Regent import views
from django.urls import path 

urlpatterns  = [
    path('', views.index, name='index'),
    path('signup/', views.index, name='signup'),
    path('login/', views.index, name='login'),
    path('cart/', views.cart, name='cart'),
    path('dashbaord', views.cart, name='dashboard'),
    path('foods', views.cart, name='foods'),
    path('beaverages', views.cart, name='beaverages'),
    path('checkout/', views.checkout, name='checkout'),
]