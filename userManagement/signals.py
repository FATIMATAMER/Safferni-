
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TypeUser

@receiver(post_save, sender=TypeUser)
def set_user_group(sender, instance, created, **kwargs):
    
    if created:
        instance.assign_group()
