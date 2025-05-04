from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)


class TripListView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


# class TripViewSet(viewsets.ModelViewSet):
#     queryset=Trip.objects.all()
#     serializer_class=TripSerializer
