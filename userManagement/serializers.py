from rest_framework import serializers
from .models import TypeUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.CharField(read_only=True)

    class Meta:
        model = TypeUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'role']
    
    def validate(self, data):
        # if data['password'] != data['password2']:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        user = TypeUser(**data)
        password = data.get('password')
        
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return data
    
    def create(self, validated_data):
        # validated_data.pop('password2')
        user = TypeUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

