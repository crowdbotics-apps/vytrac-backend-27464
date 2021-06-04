from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from Functions.MyFunctions import permision_chack
from Functions.debuging import Debugging


class DynamicSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicSerializer, self).__init__(*args, **kwargs)
        modelname = self.Meta.model.__name__.lower()
        pk = None
        user = None
        method = ''
        is_owner = False
        view_fields = None
        change_fields = None
        try:

            request = kwargs['context']['request']
            user = request.user
            if request.method == "GET":
                method = 'view'
            elif request.method == "PUT":
                method = 'change'
            elif request.method == "POST":
                method = 'add'
            elif request.method == "DELETE":
                method = 'delete'
            pk = kwargs['context']['pk']
            is_owner = modelname == 'user' and pk == user.id
        except:
            pass

        if not is_owner and len(method) > 0:
            permission = permision_chack(method, modelname, user)
            if permission['is_premited']:
                view_fields = permission['fields']
                change_fields = permission['fields']
            else:
                raise serializers.ValidationError(
                    {'permission error': permission['message']})

        fields = kwargs.pop('fields', view_fields)
        read_only_fields = kwargs.pop('read_only_fields', change_fields)

        try:
            Relations_fields = ['dates']
            for field in Relations_fields:
                permission = permision_chack('view', field[0:-1], user)
                if not is_owner and not permission['is_premited']:
                    self.fields.pop(field)
        except:
            pass

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
