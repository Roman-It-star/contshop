from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Customer

# Create your views here.
User = get_user_model()

INPUT_CLASS = (
    "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 "
    "text-slate-900 placeholder:text-slate-400 "
    "focus:outline-none focus:ring-4 focus:ring-indigo-200 focus:border-indigo-400"
)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            field.widget.attrs.setdefault("placeholder", "")

        self.fields["username"].widget.attrs["placeholder"] = "Например: roman_it"
        self.fields["email"].widget.attrs["placeholder"] = "mail@example.com"
        self.fields["phone"].widget.attrs["placeholder"] = "+7 (999) 123-45-67"