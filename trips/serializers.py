from rest_framework import serializers
from .models import Trip
from companyManagement.models import Company


class TripSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Trip
        fields = ['id', 'company', 'origin', 'destination', 'departure_date', 'time_of_travel', 'available_seats', 'price']
