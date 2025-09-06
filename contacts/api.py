from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from .serializers import ContactSerializer

from rest_framework.decorators import api_view


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {
          
          'contact us form':'/contact',
		}

	return Response(api_urls)

class ContactViewSet(viewsets.ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['post']

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


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from .serializers import ContactSerializer

# from django.core.mail import send_mail


# class ContactView(APIView):

#     throttle_scope = 'contact'
#     def post(self, request):
#         serializer = ContactSerializer(data=request.data)
#         if serializer.is_valid():
#             contact = serializer.save()

#             # 1️⃣ Notify YOU (admin)
#             admin_subject = f"📩 New Contact Message: {contact.subject}"
#             admin_message = (
#                 f"You received a new contact form submission:\n\n"
#                 f"From: {contact.name} <{contact.email}>\n"
#                 f"Subject: {contact.subject}\n\n"
#                 f"Message:\n{contact.message}\n\n"
#                 f"Sent at: {contact.created_at}"
#             )

#             send_mail(
#                 admin_subject,
#                 admin_message,
#                 settings.EMAIL_HOST_USER,  # From your Gmail
#                 [settings.EMAIL_HOST_USER],  # Send to yourself
#                 fail_silently=False,
#             )

#             # 2️⃣ Auto-reply to the user
#             user_subject = "✅ We received your message"
#             user_message = (
#                 f"Hello {contact.name},\n\n"
#                 f"Thank you for reaching out to us! We’ve received your message:\n\n"
#                 f"\"{contact.message}\"\n\n"
#                 f"Our team will get back to you as soon as possible.\n\n"
#                 f"Best regards,\nThe Support Team\n\n"
#                 f"{settings.FRONTEND_URL}"
#             )

#             send_mail(
#                 user_subject,
#                 user_message,
#                 settings.EMAIL_HOST_USER,  # From your Gmail
#                 [contact.email],  # Send to the user
#                 fail_silently=False,
#             )

#             return Response(
#                 {"message": "Your message has been received and an email confirmation has been sent."},
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
