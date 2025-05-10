from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class TypeUser(AbstractUser):
    
    phone_number = PhoneNumberField(blank=False, null=False)
    
    def assign_group(self):

        if not self.groups.exists():
            group_name="Employees" if self.is_staff else "Customers"
            group,created=Group.objects.get_or_create(name=group_name)
            self.groups.add(group)

    def __str__(self):
        return f"{self.username} ({'Employee' if self.is_staff else 'Customer'})"
    