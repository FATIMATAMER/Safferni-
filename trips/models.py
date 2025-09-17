from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from companyManagement.models import Company

from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings


class Trip(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='trips')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    # departure_time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled=models.BooleanField(default=False)
    cancel_reason=models.TextField(blank=True, null=True)
    cancelled_at=models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.available_seats is None:
            self.available_seats = self.total_seats

        if self.available_seats > self.total_seats:
            self.available_seats = self.total_seats
            
        super().save(*args, **kwargs)

    def cancel(self, reason="تم إلغاء الرحلة من قبل الشركة"):
        """
        Cancels the trip, notifies all users, and deletes bookings.
        """
        if self.is_cancelled:
            return False  # already cancelled

        # Mark trip cancelled
        self.is_cancelled = True
        self.cancel_reason = reason
        self.cancelled_at = now()
        self.save()

        # Get all bookings
        bookings = self.bookings.select_related("user")

        for booking in bookings:
            user = booking.user

            # Send notification
            message = f"""
            عزيزي {user.first_name},

            نأسف لإلغاء رحلتك رقم {self.pk}.
            السبب: {self.cancel_reason}

            شكراً لتفهمك.
            """

            send_mail(
                subject="إلغاء الرحلة",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

        # Delete bookings after notifying
        bookings.delete()

        return True
    
    def clean(self):
        if self.total_seats <= 0:
            raise ValidationError("عدد المقاعد الكلي يجب ان يكون أكبر من 0 .")
        if self.available_seats < 0:
            raise ValidationError("المقاعد المتوفر لا يمكن ان تكون سالبة .")
        
    # رحلة بديلة
    def get_next_trip(trip):
        return Trip.objects.filter(
            origin=trip.origin,
            destination=trip.destination,
            departure_date__lte=trip.departure_date + timedelta(hours=24),
            total_seats=trip.total_seats,
            is_cancelled=False,
         ).first()

    def __str__(self):
        return f"{self.pk} {self.destination} → {self.origin} ({self.departure_date}) - {self.company.company_name}"

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

