from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from .forms import UserRegisterForm, UserLoginForm
from .models import EmailConfirmed
from pamsapp.models import Profile
User = get_user_model()

# Create your views here.
def register_view(request):
    form = UserRegisterForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()

            #send email
            user = EmailConfirmed.objects.get(user = instance)
            site = get_current_site(request)
            email = instance.email
            name = instance.name
            email_body = render_to_string(
                'registration/verify_email.html',
                {
                    'name' : name,
                    'email': email,
                    'domain' : site.domain,
                    'activation_key': user.activation_key
                } 
            )
            send_mail(
                subject='Email Confirmation',
                message=email_body,
                from_email='kf.ayan17@gmail.com',
                recipient_list=[email],
                fail_silently=True
            )
            return render(request, 'registration/signup_successfull.html')
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            if _next:
                return redirect(_next)
            return redirect('pamsapp:home')
        return render(request, 'registration/login.html', {'form': form})

    else:
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def email_confirm(request, activation_key):
    user = get_object_or_404(EmailConfirmed, activation_key = activation_key)
    if user is not None:
        user.email_confirmed = True
        user.save()

        instance = User.objects.get(email = user)
        instance.is_active = True
        instance.save()
        return render(request, 'registration/verify_complete.html')


def change_pass_view(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('pamsapp:home'))
    else:
        profile = Profile.objects.get(user_id = request.user.id) 
        form = PasswordChangeForm(user = request.user)
        context = {'user': request.user, 'profile': profile, 'form':form}        
        return render(request, 'registration/change_pass.html', context)