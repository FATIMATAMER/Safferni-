from django.db import models
from trips.models import Trip
from userManagement.models import TypeUser
from datetime import datetime 

# Create your models here.


class BookingUser(models.Model):

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(TypeUser, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.IntegerField()
    booking_time = models.DateTimeField(default=datetime.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self,*args, **kwargs):
        if self.trip:
            self.total_price=self.seat_number * self.trip.price
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking: {self.passenger.username} for {self.trip} (Seat {self.seat_number})"
    
