from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.


class TypeUser(AbstractUser):
    
    phone_number = PhoneNumberField(blank=False, null=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, unique=True)
    
    def assign_group(self):

        if not self.groups.exists():
            group_name="EMPLOYEE" if self.is_staff else "CUSTOMER"
            group,created=Group.objects.get_or_create(name=group_name)
            self.groups.add(group)

    def __str__(self):
        return f"{self.username}"
    
    @property
    def role(self):
        if self.groups.filter(name="MANAGER").exists():
            return "manager"
        elif self.groups.filter(name="EMPLOYEE").exists():
            return "employee"
        else:
            return "customer"
    