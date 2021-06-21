from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from basic_app.forms import UserForm
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
import uuid
# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'

def token_send(request):
    return render(request,'token_send.html')

@login_required
def special(request):
    return HttpResponse('Congrats! You are logged in')

@login_required
def user_logout(request):
    logout(request)
    profile_obj = UserProfileInfo.objects.filter(sellerActive = 1).first()
    if profile_obj:
        profile_obj.sellerActive = 0
        profile_obj.save()
        messages.success(request, 'You are successfully logged out.')
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    # true_email = UserProfileInfo.objects.filter(sellerEmailConfirmed = True).first()
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # profile_obj = Profile.objects.create(sellertitle=user.username)
            # profile_obj.save()

            token =str(uuid.uuid4().hex)
            profile_obj = UserProfileInfo.objects.create(user = user ,sellertoken = token, sellerEmail = user.email, sellerActive = 0, sellertitle = user.username)
            profile_obj.save()


            send_mail_confirm(user.email, token)
            return redirect('/token_send/')

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'registration.html',{'user_form':user_form,'registered':registered})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                auth_login(request,user)
                profile_obj = UserProfileInfo.objects.filter(sellerActive = 0).first()
                if profile_obj:
                    profile_obj.sellerActive = 1
                    profile_obj.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account Not Active')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and password: {}'.format(username,password))
            return HttpResponse('Invalid login details')
    else:
        return render(request,'login.html',{})

def send_mail_confirm(email, token):
    subject = 'Your account need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    emai_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, emai_from, recipient_list)

def verify_email(request, token):
    profile_obj = UserProfileInfo.objects.filter(sellertoken = token).first()
    if profile_obj:
        profile_obj.sellerEmailConfirmed = True
        profile_obj.save()
        return render(request, 'verify.html')
