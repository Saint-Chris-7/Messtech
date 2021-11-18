from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid
from PIL import Image

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

class Profile(models.Model):
    customer = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    profile_pic = models.ImageField(upload_to="profile_pics",default="profile_pics/default.jpg")

    def __str__(self):
        return f"{self.customer}"

class Order(models.Model):
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE)   
    orderstatus = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    ordercode = models.UUIDField(max_length=4,auto_created=True,default=uuid.uuid4,editable=False)
    

    def __str__(self):
        return f"{self.customer}-{self.ordercode}"

class OrderItem(models.Model):
    TypeOrder = (('reserve', 'reserve'),
    ('takeaway', 'takeaway'),
    )
    ordertype = models.CharField(max_length=20,choices=TypeOrder)
    products = models.ForeignKey(Meal,on_delete=models.SET_NULL,null=True)#all foods and drinks
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.PositiveSmallIntegerField(default=True,null=True,blank=True)
    pick_up_time = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.products}"
    
    @property
    def get_total(self):
        total = self.products.price * self.quantity
        return total

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




