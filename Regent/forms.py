from django import forms

from django.db import models
from django.db.models import fields

from .models import CustomerDetails

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerDetails
        fields = "__all__"

