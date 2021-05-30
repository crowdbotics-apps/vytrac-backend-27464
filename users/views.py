from Myclasses import ItemView, ItemsView
from warnings import WarningMessage
from rest_framework import generics
from rest_framework import mixins
from MyFunctions import permision_chack
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, fields
import re
from rest_framework.generics import ListAPIView

from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.list import ListView
from django.shortcuts import render
from rest_framework import status
##
from users import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util

from django.contrib.sites.shortcuts import get_current_site
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.urls import reverse
from drf_yasg import openapi
import jwt
from django.http import HttpResponsePermanentRedirect
import os
from django.utils.encoding import DjangoUnicodeDecodeError, smart_bytes


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):

    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        link = 'http://'+current_site+relativeLink + \
            "?test="+'text______'+"?token="+str(token)
        email_body = render_to_string(
            "verify_email.html", {'name': user.username, 'link': link})
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.MyTokenObtainPairSerializer

    def post(self, request):
        data = request.data
        user = None
        is_phone = 'phone_number' in data and len(data['phone_number']) > 0
        is_email = 'email' in data and len(data['email']) > 0
        is_username = 'username' in data and len(data['username']) > 0
        if (is_phone):
            user = User.objects.get(phone_number=data['phone_number'])
        elif (is_username):
            user = User.objects.get(username=data['username'])
        elif (is_email):
            user = User.objects.get(email=data['email'])

        if (not user.is_email_verified):
            return Response({'error': 'please verfy your email'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.LoginUsersSerializer(user, many=False)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # TODO AttributeError: 'UsersSerializer' object has no attribute 'instance'
            'user': serializer.data
        })


class VerifyEmail(APIView):
    serializer_class = serializers.EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if (user.is_email_verified):
                return HttpResponseRedirect(redirect_to='https://google.com')

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            front_url = request.data.get('front_url', '')
            if (len(front_url) > 0):
                front_url += '/'if front_url[-1] != '/'else ''
            link = front_url+'?uidb64='+uidb64+'?token='+token
            email_body = render_to_string(
                "reset_password.html", {'name': user.username, 'link': link})
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password.'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSer

    def post(self, request):
        if (not request.user.id):
            return Response({'error': 'You are already loged out'})
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            return Response({"message": 'Refresh token seccesfully blacklisted.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": 'Refresh token alread blacklisted or invialid.'}, status=status.HTTP_400_BAD_REQUEST)


class WhoCanView(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsActive(permissions.BasePermission):
    message = ''

    def has_permission(self, request, view):
        message = permision_chack('view', 'user', request.user)['message']
        return permision_chack('view', 'user', request.user)['is_premited']


# class UsersView(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     # permission_classes = [IsActive]
#     queryset = User.objects.all()
#     serializer_class = serializers.UsersSerializer
#     pagination_class = PageNumberPagination
#     filter_backends = (SearchFilter, OrderingFilter)
#     search_fields = ('username', 'email', 'id')

#     def get(self, request, *args, **kwargs):
#         permission = permision_chack('view', 'user', request.user)
#         if (request.user.id and not permission['is_premited']):
#             return Response({"message": permission['message']})
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         permission = permision_chack('add', 'user', request.user)
#         if (request.user.id and not permission['is_premited']):
#             return Response({"message": permission['message']})
#         return self.create(request, *args, **kwargs)


# class UserView(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UsersSerializer

#     def get_object(self, pk,):
#         try:
#             return User.objects.get(id=pk)
#         except User.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND

#     def get(self, request, pk, format=None):
#         permission = permision_chack('view', 'user', request.user)
#         if (request.user.id and not permission['is_premited']):
#             return Response({"message": permission['message']})
#         user = self.get_object(pk)
#         serializer = serializers.UsersSerializer(user)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         mySerializer = serializers.UsersSerializerForUsers
#         if (request.user.is_staff or request.user.is_superuser):
#             mySerializer = serializers.UsersSerializerForAdmins
#         serializer = mySerializer(
#             user, data=request.data)
#         print(request.user.id)
#         permission = permision_chack('change', 'user', request.user)
#         if (not permission['is_premited']):
#             return Response({"message": permission['message']})
#         # TODOs
#         #  is_staf can updaate only is_email_verfied, is_role_verfied
#         # not is staff and user.id=request.user.id can updaate only usernmae, password, email
#         # if email updated then is_email_verfifyied =False
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(ItemView):
    MyModel = User
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer


class UsersView(ItemsView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
