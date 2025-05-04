from rest_framework import serializers
from .models import Trip
from companyManagement.models import Company


class TripSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Trip
        fields = ['id', 'company', 'origin', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'price']
