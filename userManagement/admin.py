from django.contrib import admin
from .models import TypeUser
# Register your models here.



@admin.register(TypeUser)
class TypeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'phone_number')
    list_filter = ('is_staff',)

