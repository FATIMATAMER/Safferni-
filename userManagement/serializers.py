from rest_framework import serializers
from .models import TypeUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


from django.conf import settings


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



# Reset password
# طلب اعادة تعيين كلمة المرور
class PasswordResetRequestSerializer(serializers.Serializer):
   email=serializers.EmailField(required=True)

   def validate_email(self,value):
       try:
           user=User.objects.get(email=value)

       except User.DoesNotExist:
           raise serializers.ValidationError("لا يوجد مستخدم بهذا البريد الإلكتروني")
       return value
           
       
   def save(self):
       email=self.validated_data['email']
       user=User.objects.get(email=email)
       # انشاء token
       token=default_token_generator.make_token(user)
       uid=urlsafe_base64_encode(force_bytes(user.pk))
       reset_url=f"{settings.FRONTEND_URL}/reset_password/{uid}/{token}/"
      
       
       send_mail(
              subject='إعادة تعيين كلمة المرور',
              message=f'اضغط على الرابط لإعادة تعيين كلمة المرور الخاصة بك:{reset_url}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              fail_silently=False,
                 )
      
       
   # تأكيد عملية تغيير كلمة المرور                                                                                                   
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password=serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm=serializers.CharField(required=True, write_only=True)
    def validate(self, data):
      
        if data['new_password']!=data['new_password_confirm']:
          raise serializers.ValidationError({ "new_password_confirm" : "كلمات المرور غير متطابقة" })
        try:
            uid=force_str(urlsafe_base64_decode(data['uid']))
            user=User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({ "uid" : "معرف المستخدم غير صالح" })
        if not default_token_generator.check_token(user,data['token']):
            raise serializers.ValidationError({" token" : "الرابط غير صالح او منتهي الصلاحية" })
        return data
    def save(self):
        uid=force_str(urlsafe_base64_decode(self.validated_data['uid']))
        user=User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


        
       