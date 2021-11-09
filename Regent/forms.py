from django import forms

from .models import OrderItem

class CustomerInfo(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ordertype','pick_up_time']

