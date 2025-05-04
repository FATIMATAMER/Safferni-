from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)



class CompanyViewSet(viewsets.ModelViewSet):

    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

