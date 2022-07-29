from django.conf import settings
from django.db import models
from django.utils import timezone


def upload_to(instance, filename):
    return f'images/{filename}'


class Ticket(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    state = models.CharField(max_length=10, null=False, blank=False, default='unresolved')
    ticket_photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title
