from django.db import models
from django.conf import settings
from tickets.models import Ticket, InfoFieldsMixin


class Answer(InfoFieldsMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text

