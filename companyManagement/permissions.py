from rest_framework import permissions


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='MANAGER').exists()

class IsEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='EMPLOYEE').exists()
   
class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return not (request.user.groups.filter(name='MANAGER').exists() or 
                    request.user.groups.filter(name='EMPLOYEE').exists())
   