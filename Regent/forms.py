from django import forms

from .models import Order
class CustomerInfo(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pick_up_time','ordertype']

