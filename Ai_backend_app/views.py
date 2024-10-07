from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import *
#from .searializers import *
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

##patterns = r'^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
@api_view(['POST'])
def token_obtain_pair(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        tokens = serializer.validated_data
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def token_refresh(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def validate_email(value):
    patterns = r'^[a-zA-Z][a-zA-Z0-9]*[0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

    if not re.match(patterns,value):
        raise ValidationError('email pattern not matching.')
    


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError('Password must contain at least one letter.')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[\W_]', password):  # \W matches any non-word character
        raise ValidationError('Password must contain at least one special character.')



def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        phone_no   = request.POST.get('phone_no')
        address    = request.POST.get('address')
        age        = request.POST.get('age')
        password   = request.POST.get('password')

        print(f'first_name--{first_name}')
        print(f'last_name-- {last_name}')
        print(f'email--- {email}' )
        print(f'phone_no--- {phone_no}' )
        print(f'address--- {address}' )
        print(f'age--- {age}' )
        print(f'password--- {password}' )

        try:
            validate_email(email)
        except ValidationError as e:
            return render(request, 'signup.html', {'error': str(e)})
        
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request,'signup.html',{'error':str(e)})
        
        
        if not phone_no.isdigit() or not (10 <= len(phone_no) <=12):
            return render(request,'signup.html',{'error' : 'Contact number must be between 10 and 12 digits.'})


        if Cuser.objects.filter(email=email).exists():
            return render(request,'signup.html',{'error':'Email already exists.'})
        if Cuser.objects.filter(phone_no=phone_no).exists():
            return render(request,'signup.html',{'error':'Phone number already exists.'})

        user = Cuser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            address=address,
            age=age
        )
    #     print(user)

    #     refresh = RefreshToken.for_user(user)

    #     return JsonResponse({
    #         'refresh' : str(refresh),
    #         'access' : str(refresh.access_token),
    #     })
    # return render(request,'signup.html')

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
                # user_data = Cuser.objects.get(phone_no=email_or_phone)
                # user = user_data.user
                user = Cuser.objects.get(phone_no=email_or_phone)
                
        except Cuser.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'Invalid email/phone or password. Please try again.'})

        user = authenticate(request, username=user.username, password=password)
    #     if user:
    #         refresh = RefreshToken.for_user(user)

    #         return JsonResponse({
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token),
    #         }, status=200)

    #     return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # return render(request, 'login.html')
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email/phone or password.'})

    return render(request, 'login.html')



def home(request):
    return HttpResponse('welcome to home')