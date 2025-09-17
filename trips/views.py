from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    http_method_names = ['post', 'get']

    @action(detail=True, methods=["post", 'get'], url_path="cancel")
    def cancel_trip(self, request, pk=None):
        trip = self.get_object()
        reason = request.data.get("reason", "تم إلغاء الرحلة من قبل الشركة")

        if trip.cancel(reason):
            return Response({"message": "تم إلغاء الرحلة وإعلام الركاب وحذف جميع الحجوزات"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "الرحلة ملغاة مسبقاً"}, status=status.HTTP_400_BAD_REQUEST)

