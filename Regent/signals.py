from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(User=instance)
        print("profile created")

#post_save.connect(create_profile,User)
@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwargs):
    if created == False:
        instance.Profile.save()
#.connect(create_profile,User)
