from rest_framework import serializers
from .models import BookingUser
from trips.models import Trip
from trips.serializers import TripSerializer
from django.utils import timezone
from django.db import models


class BookingSerializer(serializers.ModelSerializer):

    trip_details = TripSerializer(source='trip', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField()
    assigned_seats = serializers.SerializerMethodField()

    class Meta:
        model = BookingUser
        fields = [
            'id', 'user', 'trip', 'trip_details', 'booking_date',
            'number_of_seats', 'is_cancelled', 'cancellation_date',
            'total_price', 'assigned_seats'
        ]
        read_only_fields = ['booking_date', 'is_cancelled', 'cancellation_date']
        extra_kwargs = {
            'trip': {'write_only': True}
        }

    def get_total_price(self, obj):
        if hasattr(obj, 'total_price'):
            return obj.total_price
        return obj.trip.price * obj.number_of_seats

    def validate(self, data):

        trip = data.get('trip')
        number_of_seats = data.get('number_of_seats')
        user = self.context['request'].user
        number_of_seats = data.get('number_of_seats')


        if trip.departure_date < timezone.now():
            raise serializers.ValidationError("لا يمكنك حجز رحلة إنطلقت بالفعل")

        if number_of_seats > trip.available_seats:
            raise serializers.ValidationError(
                f"فقط {trip.available_seats} مقاعد متوفرة"
            )

        if number_of_seats <= 0:
            raise serializers.ValidationError("عدد المقاعد يجب أن يكون على الأقل 1")
        
        if BookingUser.objects.filter(user=user, trip=trip, is_cancelled=False).exists():
            raise serializers.ValidationError("لقد قمت بالفعل بالحجز بهذه الرحلة")

        # Rule 2: Maximum 5 seats per booking
        if number_of_seats > 5:
            raise serializers.ValidationError("لا يمكنك ان تقوم بحجز أكثر من 5 مقاعد في الطلب الواحد")
        
        booked_seats = BookingUser.objects.filter(trip=trip, is_cancelled=False).aggregate(
            total = models.Sum('number_of_seats')
        )['total'] or 0

        available_seats = trip.total_seats - booked_seats

        if number_of_seats > available_seats:
            raise serializers.ValidationError({
                'number_of_seats': f"فقط {available_seats} مقاعد متوفرة بهذه الرحلة "
            })

        return data
    

    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_assigned_seats(self, obj):
        # Step 1: Get all bookings for the same trip, ordered by booking date (or ID)
        all_bookings = BookingUser.objects.filter(trip=obj.trip, is_cancelled=False).order_by('booking_date', 'id')

        # Step 2: Assign seats in order
        assigned_seats = []
        current_seat = 1

        for booking in all_bookings:
            end_seat = current_seat + booking.number_of_seats - 1
            seat_range = list(range(current_seat, end_seat + 1))

            if booking.id == obj.id:
                assigned_seats = seat_range

            current_seat = end_seat + 1  # start next booking's seats

        return assigned_seats
