from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Category(models.Model):
    tags = models.CharField(max_length=12)

class Meal(models.Model):
    image = models.ImageField(upload_to="meals-pics")
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    tags = models.ForeignKey(to=Category,on_delete=models.CASCADE)

    def __str__(self):
        return f"self.name"

class Order(models.Model):
    TypeOrder = models.TextField("orderType","reserve takeaway")
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    ordercode = models.UUIDField(default=uuid.uuid4,editable=False,max_length=4)
    ordertype = models.CharField(choices=TypeOrder.choices,max_length=15)
    orderstatus = models.BooleanField(default=False,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.customer}-{self.ordercode}-{ordertype}-{orderstatus}"

class OrderItem(models.Model):
    products = models.ForeignKey(Meal,on_delete=models.SET_NULL,blank=True,null=True)#all foods and drinks
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.PositiveSmallIntegerField(default=True,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.products}"
    
    @property
    def get_total(self):
        total = self.product.price * self.qty
        return total

class Profile(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    ordercode = models.OneToOneField(OrderItem,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="priles_pics",default="defualt.jpg")

    def __str__(self):
        return f"{self.customer}"




