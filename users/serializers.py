from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2', )

    def save(self):
        user_model = get_user_model()
        user = user_model(
            username=self.validated_data.get('username'),
        )

        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')

        if password != password2:
            raise serializers.ValidationError({'passwords': 'Passwords not matched.'})
        user.set_password(password)
        user.save()
        return user


class LogInSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
        return data


class LogOutSerializer(serializers.Serializer):

    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')

        return attrs

    def save(self, **kwargs):

        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()

        except TokenError:
            self.fail('bad_token')


class UserActivitySerializer(serializers.Serializer):
    last_login = serializers.DateTimeField(allow_null=True)
    last_request_time = serializers.DateTimeField(allow_null=True)


class UserActivityQueryParamSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class SimpleUserSerializerData(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
