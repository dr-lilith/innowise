from django.conf import settings
from django.db import models


def upload_to(instance, filename):
    return f'images/{filename}'


class TicketState(models.TextChoices):
    UNRESOLVED = 'unresolved'
    RESOLVED = 'resolved'
    FROZEN = 'frozen'


class Ticket(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    state = models.CharField(
        max_length=10,
        choices=TicketState.choices,
        default=TicketState.UNRESOLVED,
    )
    ticket_photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
