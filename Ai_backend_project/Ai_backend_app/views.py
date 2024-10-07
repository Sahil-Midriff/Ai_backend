from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import *
#from .searializers import *
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from django.core.exceptions import ValidationError

def email_validation(value):
    patterns = r'^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    if not re.match(patterns,value):
        raise ValidationError('email pattern not matching.')



def signup_view(request):
    if request.method == 'POST':
        email     = request.POST.get('email') 
        thin     = request.POST.get('thin') 
        phone_no  = request.POST.get('phone_no')
        address   = request.POST.get('address')
        age       = request.POST.get('age')
        password  = request.POST.get('password')

        print('email ------',email)
        print('phone_no ------',phone_no)
        print('address ------',address)
        print('age ------',age)
        print('password ------',password)



        if Cuser.objects.filter(email=email).exists() or Cuser.objects.filter(phone_no=phone_no).exists():
            return render(request, 'signup.html', {'error': 'Email or phone number already exists.'})

        user = Cuser.objects.create(username=email, email=email,password=password)
        user.save()

        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')  
        password = request.POST.get('password')

        try:
            if '@' in email_or_phone:
                user = Cuser.objects.get(email=email_or_phone)
            else:
                user_data = Cuser.objects.get(phone_no=email_or_phone)
                user = user_data.user
        except (Cuser.DoesNotExist):
            return render(request, 'login.html', {'error_message': 'Invalid email/phone or password. Please try again.'})

        user = authenticate(request, username=user.username, password=password)
        if user is not None:



            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email/phone or password.'})

    return render(request, 'login.html')


# Create your views here.
def home(request):
    return render(request,'signup.html')

# def signup(request):
#     return render(request,'signup.html')

