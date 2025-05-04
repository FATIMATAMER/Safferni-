from rest_framework import serializers
from .models import BookingUser


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingUser
        fields = ['id', 'trip', 'passenger', 'seat_number', 'booking_time']
        read_only_fields = ['booking_time']
    
    def create(self, validated_data):
# التحقق من وجود مقاعد متاحة بصير هون 
        trip = validated_data['trip']
        if trip.available_seats <= 0:
            raise serializers.ValidationError('No available seats for this trip.')
        
    #هون مشان  تحديد المقعد 
        seat_number = validated_data['seat_number']
        
      # التحقق من أن المقعد متاح و بعدها بتم الحجز ان كان متاح 
        if BookingUser.objects.filter(trip=trip, seat_number=seat_number).exists():
            raise serializers.ValidationError('This seat is already booked.')
        
        #ناقص تحديث عدد المقاعد المتاحة
        trip.available_seats -= 1
        trip.save()

        # إنشاء الحجز
        booking = BookingUser.objects.create(**validated_data)
        return booking