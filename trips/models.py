from django.db import models
from companyManagement.models import Company


# Create your models here.
class Trip(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name="trips")
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city} ({self.company.company_name})"





