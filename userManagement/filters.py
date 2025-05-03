import django_filters
from .models import TypeUser


class UserFilter(django_filters.FilterSet):

    class Meta:
        
        model = TypeUser
        fields = {
            'username' : ['iexact', 'icontains'],
            'id' : ['exact', 'gt', 'lt', 'range'], 
        }
        