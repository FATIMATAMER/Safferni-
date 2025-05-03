from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class TypeUser(AbstractUser):
    
    phone_number = PhoneNumberField()
    password2 = models.CharField(max_length=300, blank=False, null=False)
    