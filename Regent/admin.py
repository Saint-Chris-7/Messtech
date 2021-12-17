from django.contrib import admin
from django.contrib.auth.models import User
from Regent.models import Meal,OrderItem,Profile,Order,CustomerDetails

# Register your models here.
admin.site.register(Meal)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(CustomerDetails)


