from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from App_login.models import Profile, User
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import SignUpForm
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "App_login/home.html")


def login_attempt(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            profile_obj = Profile.objects.get(user=user, is_verified=True)

            if profile_obj:
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('App_login:home'))
                else:
                    messages.success(request, 'Wrong password.')
                    return HttpResponseRedirect(reverse('App_login:login_attempt'))
            else:
                messages.success(request, 'Profile is not verified check your mail.')
                return HttpResponseRedirect(reverse('App_login:login_attempt'))

        return HttpResponseRedirect(reverse('App_login:home'))
    content = {
        'form': form
    }
    return render(request, 'App_login/login.html', context=content)


def register_attempt(request):
    form = SignUpForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_id = User.objects.get(email=email)
            try:
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user=user_id, auth_token=auth_token)
                profile_obj.save()
                send_mail_after_registration(email, auth_token)
                return HttpResponseRedirect(reverse('App_login:token_send'))
            except Exception as e:
                print(e)

    content = {
        'form': form
    }
    return render(request, 'App_login/register.html', context=content)


def success(request):
    return render(request, 'App_login/success.html')


def token_send(request):
    return render(request, 'App_login/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return HttpResponseRedirect(reverse('App_login:login_attempt'))
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return HttpResponseRedirect(reverse('App_login:login_attempt'))
        else:
            return HttpResponseRedirect(reverse('App_login:success'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('App_login:home'))


def error_page(request):
    return render(request, 'App_login/error.html')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/accounts/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
