from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .permissions import IsManager
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {

        'auth api overview' : '/',
        'create company' : 'companies/',
        'Put, Delete, and List company' : 'companies/<int:id>',
		}

	return Response(api_urls)


class CompanyViewSet(viewsets.ModelViewSet):

    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# class CompanyListView(generics.ListCreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     permission_classes = [IsManager, IsAdminUser, IsAuthenticated]



# class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     permission_classes = [IsManager, IsAdminUser, IsAuthenticated]
