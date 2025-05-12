from django.db import models
from django.core.exceptions import ValidationError
from companyManagement.models import Company


class Trip(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='trips')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    # departure_time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.available_seats is None:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def clean(self):
        if self.total_seats <= 0:
            raise ValidationError("Total seats must be greater than 0.")
        if self.available_seats < 0:
            raise ValidationError("Available seats cannot be negative.")

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_date}) - {self.company.company_name}"

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
