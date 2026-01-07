from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from apps.orders.models import Order
from .forms import RegisterForm
from django.views.decorators.http import require_POST
# Create your views here.

@login_required
def profile(request):
    orders = Order.objects.filter(customer=request.user).order_by('-id')
    return render(request, 'customers/profile.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customers:profile')
    else:
        form = RegisterForm()
    return render(request, 'customers/register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")