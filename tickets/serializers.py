from rest_framework import serializers
from.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Ticket
        fields = ('id', 'author_id', 'title', 'text', 'state', 'ticket_photo',
                  'created_date', 'is_deleted')


class TicketUpdateSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=200)
    text = serializers.CharField()
    state = serializers.CharField(max_length=10)

    class Meta(object):
        model = Ticket
        fields = ('title', 'text', 'state')


class UploadTicketPhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="post_photo", required=True)

    class Meta(object):
        model = Ticket
        fields = ['image']
