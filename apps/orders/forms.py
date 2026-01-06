from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "email", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded-lg", "placeholder": "Ваше имя"}),
            "phone": forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded-lg", "placeholder": "+7…"}),
            "email": forms.EmailInput(attrs={"class": "w-full px-3 py-2 border rounded-lg", "placeholder": "email@example.com"}),
            "comment": forms.Textarea(attrs={"class": "w-full px-3 py-2 border rounded-lg", "rows": 3, "placeholder": "Комментарий к заявке"}),
        }
