from rest_framework import serializers
from .models import BookingUser
from trips.serializers import TripSerializer
from django.utils import timezone


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

        if trip.departure_date < timezone.now():
            raise serializers.ValidationError("Cannot book a trip that has already departed.")

        if number_of_seats > trip.available_seats:
            raise serializers.ValidationError(
                f"Only {trip.available_seats} seat(s) available."
            )

        if number_of_seats <= 0:
            raise serializers.ValidationError("Number of seats must be at least 1.")

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
