from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from .models import Company
from .serializers import CompanySerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CompanyViewSet(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer


   
@api_view(['DELETE'])
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    return Response({'message': 'تم حذف الشركة بنجاح'}, status=status.HTTP_204_NO_CONTENT)

print(Company.objects.all())