from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Create your routing here.

app_name = 'customers'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
