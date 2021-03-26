from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'),
    path('change-pass/', views.change_pass_view, name='change-pass'),
    
]