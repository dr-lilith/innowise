from rest_framework import serializers
from.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Answer
        fields = ('id', 'ticket_id', 'author_id', 'text', 'created_date', 'is_deleted')


class AnswerUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)

    class Meta(object):
        model = Answer
        fields = ('text',)
