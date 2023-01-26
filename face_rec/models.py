from django.db import models
from .forms import *
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Administraion(models.Model):
    username = models.CharField(max_length=30)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=13)

class Enroll(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Arid_no = models.CharField(max_length=12)
    img = models.ImageField(upload_to='images')
