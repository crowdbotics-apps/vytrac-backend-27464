from django.core.exceptions import EmptyResultSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from MyFunctions import permision_chack
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from users.models import User

from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from users.models import User
from drf_queryfields import QueryFieldsMixin


def convert_to_list(django_boject):
    flat_object = django_boject.values_list('codename', flat=True)
    return list(flat_object)


class DynamicSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # def create(self, validated_data, **kwargs):
    # user = self.context['request'].user
    # modelname = self.Meta.model.__name__.lower()
    # permission = permision_chack('add', modelname, user)
    # if (not permission['is_premited']):
    #     raise serializers.ValidationError(
    #         {'permission error': permission['message']})
    # print('======================')
    # print(validated_data)
    # print('======================')
    # return validated_data

    def __init__(self, * args, **kwargs):

        modelname = self.Meta.model.__name__.lower()
        is_GET = "GET" in str(kwargs['context']['request'])
        is_PUT = "PUT" in str(kwargs['context']['request'])
        is_POST = "POST" in str(kwargs['context']['request'])
        is_DELETE = "DELETE" in str(kwargs['context']['request'])

        user = kwargs['context']['request']._user
        permissions = convert_to_list(user.user_permissions.all())
        for group in user.groups.all():
            groups_permissions = convert_to_list(group.permissions.all())
            permissions += list(groups_permissions)
        permissions = list(filter(lambda x: 'field' in x, permissions))
        view_fields = []
        change_fields = []

        super(DynamicSerializer, self).__init__(*args, **kwargs)

        if(is_PUT):
            permission = permision_chack('change', modelname, user)
            if (permission['is_premited']):
                change_fields = permission['fields']
            else:
                raise serializers.ValidationError(
                    {'permission error': permission['message']})
        if(is_GET):
            permission = permision_chack('view', modelname, user)
            if (permission['is_premited']):
                view_fields = permission['fields']
            else:
                raise serializers.ValidationError(
                    {'permission error': permission['message']})
        view_fields = None
        change_fields = None
        fields = kwargs.pop('fields', view_fields)
        read_only_fields = kwargs.pop('read_only_fields', change_fields)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if read_only_fields is not None:
            for f in read_only_fields:
                try:
                    self.fields[f].read_only = True
                except:
                    pass


class ItemsView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    # permission_classes = [IsActive]

    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ItemView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    MyModel = User

    def get_object(self, pk,):
        try:
            return self.MyModel.objects.get(id=pk)
        except self.MyModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        # TODO serilizer delete permision_chack
        # permission = permision_chack('delete', self.ModelName, request.user)
        # if (not permission['is_premited']):
        #     return Response({"message": permission['message']})
        date = self.MyModel.objects.get(id=pk)
        date.delete()
        serializer = self.serializer_class(date)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        date = self.get_object(pk)
        serializer = self.serializer_class(
            date, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
