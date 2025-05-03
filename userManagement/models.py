from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.

class TypeUser(AbstractUser):
    
    phone_number=models.CharField(max_length=15,blank=True,null=True)

    def assign_group(self):

        if not self.groups.exists():
            group_name="Employees" if self.is_staff else "Customers"
            group,created=Group.objects.get_or_create(name=group_name)
            self.groups.add(group)

    def __str__(self):
        return f"{self.username} ({'Employee' if self.is_staff else 'Customer'})"
    