from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields = ['id', 'full_name', 'email', 'subject_of_message', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

