from rest_framework import permissions

from Functions.MyFunctions import permision_chack
from Functions.MyViews import ItemView, ItemsView
##
from users import serializers
from .models import User
from rest_framework import permissions

from Functions.MyFunctions import permision_chack
from Functions.MyViews import ItemView, ItemsView
##
from users import serializers
from .models import User


class WhoCanView(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsActive(permissions.BasePermission):
    message = ''

    def has_permission(self, request, view):
        message = permision_chack('view', 'user', request.user)['message']
        return permision_chack('view', 'user', request.user)['is_premited']


class UserView(ItemView):
    MyModel = User
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer


class UsersView(ItemsView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    search_fields = '__all__'
