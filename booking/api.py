from rest_framework import generics, serializers
from .models import Trip, BookingUser
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {

        'auth api overview' : '/',
        'list and create new booking' : 'list/',
        'Update, retreive and delete a bookings' : 'create/',
        'List authenticated user bookings' : 'user/bookings',
		}

	return Response(api_urls)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # يجب أن يكون المستخدم مسجلاً للدخول إجبارية مسجل دخول 
def create_booking(request):

    trip_id = request.data.get('trip_id')
    seat_number = request.data.get('seat_number')

 # تحقق من وجود الرحلة
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

  # تحقق من وجود مقاعد متاحة
    if trip.available_seats <= 0:
        return Response({"detail": "No available seats."}, status=status.HTTP_400_BAD_REQUEST)
  # التحقق ان كان المقعد محوز ام لا 
    if BookingUser.objects.filter(trip=trip, seat_number=seat_number).exists():
        return Response({"detail": "Seat already booked."}, status=status.HTTP_400_BAD_REQUEST)

  # إنشاء الحجز
    booking = BookingUser.objects.create(
        trip=trip,
        passenger=request.user,
        seat_number=seat_number
    )

    # تحديث عدد المقاعد المتاحة
    trip.available_seats -= 1
    trip.save()

    # إعادة استجابة بنجاح الحجز
    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingCreateView(generics.CreateAPIView):

    queryset = BookingUser.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        trip_id = request.data.get('trip')
        seat_number = request.data.get('seat_number')
        trip = Trip.objects.get(id=trip_id)
        
        # تحقق من المقاعد المتاحة
        if trip.available_seats > 0:
            booking = super().create(request, *args, **kwargs)
            trip.available_seats -= 1  # تقليل المقاعد المتاحة
            trip.save()
            return booking
        else:
            return Response({"detail": "No available seats"}, status=status.HTTP_400_BAD_REQUEST)
        

class BookingListView(generics.ListAPIView):

    queryset = BookingUser.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class UserBookingsView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookingUser.objects.filter(passenger=self.request.user)
    
