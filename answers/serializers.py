from users.serializers import UserSerializer
from tickets.serializers import TicketSerializer
from rest_framework import serializers
from rest_framework import serializers
from.models import *


class AnswerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Answer
        fields = ('id', 'ticket_id', 'author_id', 'text', 'created_date', 'is_deleted')


class AnswerUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)

    class Meta(object):
        model = Answer
        fields = ('text',)

    def update(self, answer, validated_data):
        answer.text = validated_data['text']
        answer.save()
        return answer
