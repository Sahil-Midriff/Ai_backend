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
    

class csv_files(models.Model):
    user                = models.ForeignKey(Cuser,on_delete=models.CASCADE)
    csv_name            = models.CharField(max_length=100,null=True,blank=True)
    csv_size            = models.CharField(max_length=100,null=True,blank=True)
    csv_file            = models.FileField(upload_to='csv_files/', null=True, blank=True)  # Store actual file

    def __str__(self):
        return f"{self.csv_name} ----  {self.user}"