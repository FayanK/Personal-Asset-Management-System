from django.shortcuts import render
from .models import *
from accounts.models import CustomUser
from pamsapp.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


