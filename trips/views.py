from django.shortcuts import render
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Trip
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

 
# Create your views here.
class CancelTripView(APIView):
    def post(self, request, pk):
     try:
        trip=Trip.objects.get(id = pk)

        if trip.is_cancelled:
            return Response({'message' :'الرحلة ملغاة مسبقاً' }, status=400)
        
        trip.is_cancelled=True
        trip.cancel_reason=request.data.get('reason','تم إلغاء الرحلة من قبل الشركة')
        trip.cancelled_at=now()
        trip.save()
        
        bookings =trip.bookings.select_related('user')
        next_trip=Trip.get_next_trip(trip)

        
        for booking in bookings:
            user =booking.user
            booking.is_cancelled=True
            booking.save()
            
            if next_trip: 
                  message=f"""
                     عزيزي  {user.first_name},
                     نأسف لإلغاء رحلتك رقم {trip.pk},
                     السبب : {trip.cancel_reason}
                     يوجد اقتراح لرحلة بديلة رقم {next_trip.pk}:
                     - الإنطلاق : {next_trip.origin}
                     - الوجهة : {next_trip.destination}
                     - الوقت والتاريخ : {next_trip.departure_date.strftime('%Y-%m-%d %H:%M')}
                
                         إذا كنت مهتم بالحجز لا تفوت الفرصة وقم بزيارة موقعنا
                     """
            else :
                  message=f""" {user.first_name} عزيزي , 
                  لقد تم إلغاء رحلتك بسبب {trip.cancel_reason},
                  نأسف لذلك وسنقوم بإعلامك في موعد أقرب رحلة بديلة في حال وجودها """

                 

            send_mail(
                     subject= "الغاء الرحلة",
                     message=message,
                     from_email= settings.EMAIL_HOST_USER,
                     recipient_list=[user.email],
                     fail_silently=False,)
        return Response({'message':'تم إلغاء الرحلة وإعلام الركاب بذلك'},status=200)
     except Trip.DoesNotExist:
        return Response({'message':'الرحلة غير موجودة'}, status=200)
      
