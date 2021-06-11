from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (
    ModelSerializer,
)

from Functions.DynamicSer import DynamicSerializer
from patients.views import patients
from timesheets.urls import StatisticSer
from ..models import User, Availablity

class PasswordSer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        partial_update = True

class LoginUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class EmailVerificationSerializer(ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LogoutSer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=555)

    class Meta:
        fields = ['refresh_token']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    front_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class MyTokenObtainPairSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    username = serializers.CharField(
        min_length=3, required=False, write_only=True)
    phone_number = serializers.CharField(
        min_length=1, required=False, write_only=True)
    email = serializers.CharField(
        min_length=1, required=False, write_only=True)

    class Meta:
        fields = ['username', 'phone_number', 'email', 'password']

    # def validate(self, attrs):
    #     try:
    #         password = attrs.get('password')
    #         token = attrs.get('token')
    #         uidb64 = attrs.get('uidb64')

    #         id = force_str(urlsafe_base64_decode(uidb64))

    #         user = User.objects.get(id=id)
    #         if not PasswordResetTokenGenerator().check_token(user, token):
    #             raise AuthenticationFailed('The reset link is invalid', 401)

    #         user.set_password(password)
    #         user.save()

    #         return (user)
    #     except Exception as e:
    #         raise AuthenticationFailed('The reset link is invalid', 401)
    #     return super().validate(attrs)
