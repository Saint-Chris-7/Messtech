from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.fields import NullBooleanField
#from PIL import Image

# Create your models here.
class Meal(models.Model):
    TAGS =(
        ('foods', 'foods'),
        ('beverages', 'beverages'),
        )
    image = models.ImageField(upload_to="meals-pics")
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    tags = models.CharField(max_length=10, choices=TAGS)

    def __str__(self):
        return f"{self.name}"
    @property
    def imageURL(self):
        try:
           url = self.image.url
        except:
            url="" 
        return url
    

class Profile(models.Model):
    customer = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return f"{self.customer}"

class Order(models.Model):
    customer = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)   
    orderstatus = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    ordercode = models.IntegerField(null=True)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems= self.orderitem_set.all()
        total= sum([item.quantity for item in orderitems])
        return total
    

    def __str__(self):
        return f"{self.id}"
    def save(self, *args,**kwargs):
        #if self.ordercode == "":
        self.ordercode= self.id
        return super().save(*args,**kwargs)

class OrderItem(models.Model):
    TypeOrder = (('reserve', 'reserve'),
    ('takeaway', 'takeaway'),
    )
    ordertype = models.CharField(max_length=20,choices=TypeOrder)
    products = models.ForeignKey(Meal,on_delete=models.SET_NULL,null=True)#all foods and drinks
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    orderitemID = models.PositiveSmallIntegerField(auto_created=True,null=True)

    def __str__(self):
        return f"{self.order}"
    
    @property
    def get_total(self):
        total = self.products.price * self.quantity
        return total

class CustomerDetails(models.Model):
    name = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    ordertype = models.CharField(max_length=20)
    table = models.IntegerField(null=True)
    time = models.TimeField()

    def __str__(self):
        return f"Name={self.name}       OrderNo:- {self.order}"
    

  
        
            
        
        





"""
    def save(self):
        img = Image.open(self.profile_pic.path) # Open image 
        # resize image
        if img.height > 100 or img.width > 100:
            output_size = (250, 150)
            img.thumbnail(output_size) # Resize image
            img.save(self.profile_pic.path) # Save it again and override the larger image
        return super().save()
        """




