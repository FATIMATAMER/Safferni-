from django.db import models

# Create your models here.


class Company(models.Model):
    
    company_name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    phone_number=models.CharField(max_length=15)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return  self.company_name

