from django.db import models

# Create your models here.

subject_choices = [
    ("complains","شكوى"),
    ("criticism","نقد بناء"),
    ("other","شيء أخر"),
]
class Contact(models.Model):

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject_of_message = models.CharField(max_length=50, choices=subject_choices, default="شكوى")
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"