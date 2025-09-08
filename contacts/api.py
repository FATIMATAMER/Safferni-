from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'contact us form': '/contact',
    }
    return Response(api_urls)


class ContactViewSet(viewsets.ModelViewSet):
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # 1️⃣ Notify admin
        admin_subject = f"📩 New Contact Message: {contact.subject_of_message}"
        admin_message = (
            f"You received a new contact form submission:\n\n"
            f"From: {contact.full_name} <{contact.email}>\n"
            f"Subject: {contact.subject_of_message}\n\n"
            f"Message:\n{contact.message}\n\n"
            f"Sent at: {contact.created_at}"
        )
        send_mail(
            admin_subject,
            admin_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # 2️⃣ Auto-reply to user
        user_subject = "✅ We received your message"
        user_message = (
            f"مرحبا {contact.full_name},\n\n"
            f"شكرا ل تواصلك معنا. لقد تلقينا رسالتك :\n\n"
            f"\"{contact.message}\"\n\n"
            f"سيتم التواصل معك في اقرب فرصة ممكنة.\n\n"
            f"{settings.FRONTEND_URL}"
        )
        send_mail(
            user_subject,
            user_message,
            settings.EMAIL_HOST_USER,
            [contact.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Your message has been received and a confirmation email has been sent."},
            status=status.HTTP_201_CREATED
        )