from Regent import views
from django.urls import path 

urlpatterns  = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('delete/<int:id>/', views.delete_cart, name='delete'),
    path('dashbaord', views.dashboard, name='dashboard'),
    path('foods', views.foods, name='foods'),
    path('beverages', views.beverages, name='beverages'),
    path('checkout/', views.checkout, name='checkout'),
]