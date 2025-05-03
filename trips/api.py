from rest_framework import viewsets, generics
from .models import Trip
from .serializers import TripSerializer
from .permissions import IsManager, IsEployee
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)


class TripViewSet(viewsets.ModelViewSet):
    
    queryset=Trip.objects.all()
    serializer_class=TripSerializer
    permission_classes = [IsManager, IsAdminUser, IsAuthenticated]


# class TripView(generics.RetrieveUpdateDestroyAPIView):

#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [IsAuthenticated, IsManager]
#         return [permission() for permission in permission_classes]
    