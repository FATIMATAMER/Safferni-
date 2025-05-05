from rest_framework.response import Response
from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer
from rest_framework import viewsets, generics
from .models import Trip
from .serializers import TripSerializer
from .permissions import IsManager, IsEployee
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)

from rest_framework.decorators import api_view


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {

        'auth api overview' : '/',
        'list and create new trip' : 'create/',
        'Update, retreive and delete a trip' : 'detail/<int:pk>/',
		}

	return Response(api_urls)


class TripListView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsManager, IsAdminUser, IsAuthenticated]



class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsManager, IsAdminUser, IsAuthenticated]


# class TripViewSet(viewsets.ModelViewSet):
    
#     queryset=Trip.objects.all()
#     serializer_class=TripSerializer
#     permission_classes = [IsManager, IsAdminUser, IsAuthenticated]


# class TripView(generics.RetrieveUpdateDestroyAPIView):

#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [IsAuthenticated, IsManager]
#         return [permission() for permission in permission_classes]
    
