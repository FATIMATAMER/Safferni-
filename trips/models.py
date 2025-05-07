from django.db import models
from companyManagement.models import Company
from datetime import time


# Create your models here.

class Trip(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='trips')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    time_of_travel = models.TimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField(default=total_seats)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_date}) - {self.company.company_name}"
    
    class Meta:
        
        verbose_name = "Trip"
        verbose_name_plural = "Trips"



