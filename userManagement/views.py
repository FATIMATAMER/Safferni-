from django.shortcuts import render
from .serializers import PasswordResetRequestSerializer,PasswordResetConfirmSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class PasswordResetRequestView(APIView):
    def post(self,request):
        serializer=PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "message":"تم إرسال رابط اعادة تعيين كلمة المرور الي بريدك الإلكتروني" },status=200)
        
        return Response(serializer.errors,status=400)
    
class PasswordResetConfirmRequestView(APIView):
    def post(self,request):
        serializer=PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ "message":" تمت عملية إعادة تعيين كلمة المرور بنجاح" }, status=400)
        
        return Response(serializer.errors,status=400)
    

    