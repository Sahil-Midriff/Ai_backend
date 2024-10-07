from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Cuser(AbstractUser):
    phone_no          = models.CharField(max_length=10,unique=True,null=True,blank=True)
    access            = models.CharField(max_length=2000,unique=True,null=True,blank=True)
    address           = models.TextField(null=True,blank=True)
    age               = models.IntegerField(null=True,blank=True)
    status            = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return f"{self.id} -- {self.username}"