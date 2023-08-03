from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
