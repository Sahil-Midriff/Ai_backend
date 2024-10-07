from django.urls import path
from .views import *

urlpatterns = [
    path('home/',    home,name='home'),
    path('signup/',  signup_view,name='signup'),
    path('login/',   signup_view,name='signup'),
    # path('login/',   signup_view,name='signup'),
]