from rest_framework import serializers
from .models import BookingUser
from trips.serializers import TripSerializer
from django.utils import timezone
from datetime import datetime


class BookingSerializer(serializers.ModelSerializer):

    trip_details = TripSerializer(source='trip', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField()
    assigned_seats = serializers.SerializerMethodField()
    
    class Meta:

        model = BookingUser
        fields = [
            'id', 'user', 'trip', 'trip_details', 'booking_date',
            'number_of_seats', 'is_cancelled', 'cancellation_date',  'total_price', 'assigned_seats'
        ]
        read_only_fields = ['booking_date', 'is_cancelled', 'cancellation_date']
        extra_kwargs = {
            'trip': {'write_only': True}
        }

    def get_total_price(self, obj):

        """Calculate total price for all remaining seats"""
        # If we annotated in the queryset
        if hasattr(obj, 'total_price'):
            return obj.total_price
        # Fallback calculation
        return obj.trip.price * obj.number_of_seats

    def validate(self, data):

        trip = data.get('trip')
        number_of_seats = data.get('number_of_seats')
        
        if trip.departure_date < timezone.now():
            raise serializers.ValidationError("Cannot book for past dates.")
        
        if trip.departure_date == timezone.now():
            if trip.departure_date < timezone.now():
                raise serializers.ValidationError("The trip has already departed.")
        
        if number_of_seats > trip.available_seats:
            raise serializers.ValidationError(
                f"Only {trip.available_seats} seat(s) available."
            )
        
        if number_of_seats <= 0:
            raise serializers.ValidationError("Number of seats must be at least 1.")
            
        return data
    
 
    