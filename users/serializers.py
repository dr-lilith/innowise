from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'username', 'description', 'avatar')
        extra_kwargs = {'password1': {'write_only': True}}


class RegistrationSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta(object):
        model = User
        fields = ('email', 'password', 'username', 'avatar', 'date_joined')
        extra_kwargs = {'password1': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'].lower(),
            username=self.validated_data['username']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class UploadAvatarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="avatar", required=True)

    class Meta(object):
        model = User
        fields = ('image',)
