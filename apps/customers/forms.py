from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

# Create your views here.

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'password1', 'password2']