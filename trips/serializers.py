from rest_framework import serializers
from .models import Trip
from companyManagement.models import Company


class TripSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'company', 'company_name', 'origin', 'destination', 'departure_date', 'total_seats', 'available_seats', 'price']
