# import datetime
# from warnings import WarningMessage
# from rest_framework import generics
# from rest_framework import mixins
# from Functions.MyFunctions import permision_chack
# from django.contrib.auth.models import Permission
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.auth.models import Group
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django.db.models import Q
# import re
# from rest_framework.generics import ListAPIView

# from django.http.response import HttpResponseRedirect
# from django.template.loader import render_to_string
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.http import urlsafe_base64_encode
# from rest_framework import generics, mixins, permissions

# from rest_framework.views import APIView
# from django.views.generic.list import ListView
# from django.shortcuts import render
# from rest_framework import status
# ##
# from . import serializers
# from .models import Date, DateType
# from users.models import User
# import datetime
# from dateutil import parser


# class IsActive(permissions.BasePermission):
#     message = ''

#     def has_permission(self, request, view):
#         message = permision_chack('view', 'user', request.user)['message']
#         return permision_chack('view', 'user', request.user)['is_premited']


# class DatesView(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     # permission_classes = [IsActive]
#     queryset = Date.objects.all()
#     serializer_class = serializers.DateSer
#     pagination_class = PageNumberPagination
#     filter_backends = (SearchFilter, OrderingFilter)
#     search_fields = ('title', 'date_type', 'start'
#                      # ,'end'
#                      )

#     def get(self, request, *args, **kwargs):
#         permission = permision_chack('view', 'date', request.user)
#         if (request.user.id and not permission['is_premited']):
#             return Response({"message": permission['message']})
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         date_type = DateType.objects.get(id=request.data['date_type']).name
#         # permission = permision_chack('add', 'date', request.user)
#         messages = []
#         users_list = request.data.getlist('users')
#         if (not request.user.is_staff or not request.user.is_superuser):
#             users_list.append(request.user.id)
#         users = User.objects.filter(id__in=users_list)
#         for user in users:
#             schadule = Date.objects.fliter(users__contains=user)
#             is_busy = schadule.filter(Q(start__lte=request.data['start']) and Q(
#                 end__gte=request.data['end']))
#             serializer = serializers.DateSer(is_busy, many=True)
#             if (is_busy.exists()):
#                 messages.append(
#                     {user.username+" is already bussying during": serializer.data})

#         is_start_before_now = (parser.parse(
#             request.data['start'])) <= datetime.datetime.now()
#         is_end_before_now = parser.parse(
#             request.data['end']) <= datetime.datetime.now()
#         if (is_start_before_now or is_end_before_now):
#             return Response({'message': "You can't create "+date_type+" for start or end before now"})

#             # others = User.objects.fliter(id=request.data['users'])
#             # TODO
#             # dates = Date.objects.filter(
#             #     Q(start_gte=now) | Q(end_gte=now))
#             # your_schadule = Date.objects.filter(
#             #     Q(created_by=you) | Q(date_with=you))
#             # other_schadule = Date.objects.filter(
#             #     Q(created_by=other) | Q(date_with=other))

#         # if (request.data['start' or 'end']>=now):
#         #     serializer = serializers.DateSer(other_schadule, many=True)
#         #     messages.append(
#         #         {"error": 'you can not create '+date_type' for a date preceeding now'})

#         # if (is_other_busy.exists()):
#         #     serializer = serializers.DateSer(other_schadule, many=True)
#         #     messages.append(
#         #         {other.username+" not available durring": serializer.data})
#         # if (is_you_busy.exists()):
#         #     serializer = serializers.DateSer(your_schadule, many=True)
#         #     messages.append({"You already busy durring ": serializer.data})

#         # if (request.user.id and not permission['is_premited']):
#         #     return Response({"message": permission['message']})
#         # if(len(messages) > 0):
#         #     return Response({"messages": messages})

#         # newDate = Date.objects.create(created_by=request.user, start=request.data['start'], end=request.data['end'],
#         #                               date_with=other, title=request.data['title'], description=request.data['description'])
#         # if(not you.is_superuser and not you.is_staff):
#         #     newDate.users.add(you)
#         # newDate.save()
#         # return Response(serializers.DateSer(newDate).data)

#         return self.create(request, *args, **kwargs)


# class DateView(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#     queryset = Date.objects.all()
#     serializer_class = serializers.DateSer

#     def get_object(self, pk,):
#         try:
#             return Date.objects.get(id=pk)
#         except Date.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND

#     def get(self, request, pk, format=None):
#         permission = permision_chack('view', 'date', request.user)
#         if (request.user.id and not permission['is_premited']):
#             return Response({"message": permission['message']})
#         payment = self.get_object(pk)
#         serializer = serializers.PaymentSer(payment)
#         return Response(serializer.data)

#     # def delete(self, request, pk, format=None):
#     #     permission = permision_chack('view', 'date', request.user)
#     #     if (request.user.id and not permission['is_premited']):
#     #         return Response({"message": permission['message']})
#     #     date = Date.objects.get(id=pk)
#     #     date.objects.filter(id=pk).delete()
#     #     serializer = serializers.DateSer(date)
#     #     return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         date = self.get_object(pk)
#         mySerializer = serializers.DateSerForUsers
#         if (request.user.is_staff or request.user.is_superuser):
#             mySerializer = serializers.DateSerForAdmins
#         # TODO test
#         serializer = mySerializer(
#             date, data=request.data)
#         print(request.user.id)
#         permission = permision_chack('change', 'user', request.user)
#         if (not permission['is_premited']):
#             return Response({"message": permission['message']})

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
