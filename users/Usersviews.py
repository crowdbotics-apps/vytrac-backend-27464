##
from rest_framework import permissions, status
from rest_framework.response import Response

from Functions.MyViews import ItemView, ItemsView
from Functions.Permissions import permision_chack, get_user_permissions
##
from Functions.debuging import Debugging
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

    def get(self, request, pk):
        setattr(request,'is_owner',pk == request.user.id)
        return super().get(request, pk,)

    def put(self, *args,**kwargs):
        user = self.request.user
        permissions = get_user_permissions(user)
        is_permited = 'add_user' or 'update_user' or 'update_email' in permissions
        # ?TODO test is_permited and is not permited
        if permissions or not user.is_staff or not user.is_superuser:
            self.serializer_class = serializers.UpdateUsersSerializer
            # if 'email' in self.request.data:
                # TODO send to the admins a request to update to this email
                # Debugging(self.request.data, color='green')
        return super().put(*args,**kwargs)

class UsersView(ItemsView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    search_fields = '__all__'


