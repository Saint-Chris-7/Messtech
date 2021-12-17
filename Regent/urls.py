from Regent import views
from django.urls import path 

urlpatterns  = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('receipt/', views.order_receipt, name='receipt'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('transaction/', views.transaction, name='transaction'),
    path('daraja/stk-push/', views.stk_push_callback, name='mpesa_stk_push_callback'),

]