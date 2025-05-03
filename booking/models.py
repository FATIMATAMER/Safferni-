from django.db import models
from trips.models import Trip
from userManagement.models import TypeUser
# Create your models here.

class BookingUser(models.Model):
    
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="bookings")
    user=models.ForeignKey(TypeUser, on_delete=models.CASCADE, related_name="bookings")
    seat_count=models.PositiveSmallIntegerField(default=1)
    total_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self,*args, **kwargs):
        if self.trip:
            self.total_price=self.seat_count * self.trip.price
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f" Booking for {self.user.username} - Seats : {self.seat_count} - Total price : {self.total_price}"


