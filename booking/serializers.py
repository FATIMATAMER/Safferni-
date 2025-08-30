# booking/serializers.py
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
        read_only_fields = ['booking_date', 'cancellation_date']
        extra_kwargs = {
            'trip': {'write_only': True}
        }
    
    # **ملاحظة:** تم إزالة 'is_cancelled' من read_only_fields
    # لكي يتمكن طلب الـ PATCH من تحديثه.

    def get_total_price(self, obj):
        if hasattr(obj, 'total_price'):
            return obj.total_price
        return obj.trip.price * obj.number_of_seats

    def validate(self, data):
        # **التعديل هنا:**
        # الحصول على كائن الرحلة. إذا كان التحديث (PATCH)، خذها من self.instance.
        # إذا كان الحجز جديدًا (POST)، خذها من البيانات القادمة في الطلب.
        trip = self.instance.trip if self.instance else data.get('trip')
        number_of_seats = data.get('number_of_seats')
        user = self.context['request'].user
        number_of_seats = data.get('number_of_seats')

        # إذا لم يتم العثور على الرحلة، أرسل خطأ.
        if trip is None:
            raise serializers.ValidationError({"detail": "Trip not found in validation data."})

        # **ملاحظة:** الكود التالي أصبح آمناً الآن
        # لأننا تأكدنا من أن `trip` ليس None
        
        # Rules for new bookings (POST) and updates (PATCH)
        # Check if is_cancelled is present in data (only for PATCH request)
        if 'is_cancelled' in data and data.get('is_cancelled') is True:
            # Logic specific to cancellation
            if trip.departure_date < timezone.now():
                raise serializers.ValidationError({"is_cancelled": "Cannot cancel a booking for a trip that has already departed."})
            return data
        
        # Rules for new bookings (POST) - if 'trip' is in data, it's a new booking
        if 'trip' in data:
            number_of_seats = data.get('number_of_seats')
            user = self.context['request'].user
            
            if trip.departure_date < timezone.now():
                raise serializers.ValidationError("Cannot book a trip that has already departed.")

            if number_of_seats > trip.available_seats:
                raise serializers.ValidationError(
                    f"Only {trip.available_seats} seat(s) available."
                )

            if number_of_seats <= 0:
                raise serializers.ValidationError("Number of seats must be at least 1.")
            
            if BookingUser.objects.filter(user=user, trip=trip, is_cancelled=False).exists():
                raise serializers.ValidationError("You have already booked in this trip.")

            if number_of_seats > 5:
                raise serializers.ValidationError("You cannot book more than 5 seats at once.")
            
            booked_seats = BookingUser.objects.filter(trip=trip, is_cancelled=False).aggregate(
                total = models.Sum('number_of_seats')
            )['total'] or 0

            available_seats = trip.total_seats - booked_seats

            if number_of_seats > available_seats:
                raise serializers.ValidationError({
                    'number_of_seats': f"Only {available_seats} seats are available on this trip."
                })

        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_assigned_seats(self, obj):
        all_bookings = BookingUser.objects.filter(trip=obj.trip, is_cancelled=False).order_by('booking_date', 'id')

        assigned_seats = []
        current_seat = 1

        for booking in all_bookings:
            end_seat = current_seat + booking.number_of_seats - 1
            seat_range = list(range(current_seat, end_seat + 1))

            if booking.id == obj.id:
                assigned_seats = seat_range

            current_seat = end_seat + 1

        return assigned_seats
    
from rest_framework import serializers
# from .models import BookingUser
# from trips.models import Trip
# from trips.serializers import TripSerializer
# from django.utils import timezone
# from django.db import models


# class BookingSerializer(serializers.ModelSerializer):

#     trip_details = TripSerializer(source='trip', read_only=True)
#     user = serializers.StringRelatedField(read_only=True)
#     total_price = serializers.SerializerMethodField()
#     assigned_seats = serializers.SerializerMethodField()

#     class Meta:
#         model = BookingUser
#         fields = [
#             'id', 'user', 'trip', 'trip_details', 'booking_date',
#             'number_of_seats', 'is_cancelled', 'cancellation_date',
#             'total_price', 'assigned_seats'
#         ]
#         read_only_fields = ['booking_date', 'is_cancelled', 'cancellation_date']
#         extra_kwargs = {
#             'trip': {'write_only': True}
#         }

#     def get_total_price(self, obj):
#         if hasattr(obj, 'total_price'):
#             return obj.total_price
#         return obj.trip.price * obj.number_of_seats

#     def validate(self, data):

#         trip = data.get('trip') or getattr(self.instance, "trip", None)
#         number_of_seats = data.get('number_of_seats')
#         user = self.context['request'].user
#         number_of_seats = data.get('number_of_seats')

#         if not trip and not self.instance:
#             return data
        
#         if trip.departure_date < timezone.now():
#             raise serializers.ValidationError("Cannot book a trip that has already departed.")

#         if number_of_seats > trip.available_seats:
#             raise serializers.ValidationError(
#                 f"Only {trip.available_seats} seat(s) available."
#             )

#         if number_of_seats <= 0:
#             raise serializers.ValidationError("Number of seats must be at least 1.")
        
#         if BookingUser.objects.filter(user=user, trip=trip, is_cancelled=False).exists():
#             raise serializers.ValidationError("You have already booked in this trip.")

#         # Rule 2: Maximum 5 seats per booking
#         if number_of_seats > 5:
#             raise serializers.ValidationError("You cannot book more than 5 seats at once.")
        
#         booked_seats = BookingUser.objects.filter(trip=trip, is_cancelled=False).aggregate(
#             total = models.Sum('number_of_seats')
#         )['total'] or 0

#         available_seats = trip.total_seats - booked_seats

#         if number_of_seats > available_seats:
#             raise serializers.ValidationError({
#                 'number_of_seats': f"Only {available_seats} seats are available on this trip."
#             })

#         return data
    

    
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)
    
#     def get_assigned_seats(self, obj):
#         # Step 1: Get all bookings for the same trip, ordered by booking date (or ID)
#         all_bookings = BookingUser.objects.filter(trip=obj.trip, is_cancelled=False).order_by('booking_date', 'id')

#         # Step 2: Assign seats in order
#         assigned_seats = []
#         current_seat = 1

#         for booking in all_bookings:
#             end_seat = current_seat + booking.number_of_seats - 1
#             seat_range = list(range(current_seat, end_seat + 1))

#             if booking.id == obj.id:
#                 assigned_seats = seat_range

#             current_seat = end_seat + 1  # start next booking's seats

#         return assigned_seats