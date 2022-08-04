from django.db import models
from django.utils import timezone
from tickets.models import Ticket
from django.conf import settings


class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.TextField(max_length=200, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.text

