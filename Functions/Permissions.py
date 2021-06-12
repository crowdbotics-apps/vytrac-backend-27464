import re

from colorama import Fore, Back
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from Functions.debuging import Debugging
from Functions.make_fields_permissions import make_fields_permissions


def convert_to_list(django_boject):
    flat_object = django_boject.values_list('codename', flat=True)
    return list(flat_object)


def convert_to_fieldname(action, field):
    fieldname = re.search(
        rf'({action})(_)(\w+)(.)(\w+)(_field)', field, re.IGNORECASE)
    return fieldname.group(5)


def get_user_permissions(user):
    user_permissions = convert_to_list(user.user_permissions.all())
    for group in user.groups.all():
        groups_permissions = convert_to_list(group.permissions.all())
        user_permissions += list(groups_permissions)
    return user_permissions


def permision_chack(action, modelname, user):
    is_permited = False
    message = ''
    fields = None
    required_permission = action + '_' + modelname
    user_permissions = []
    try:
        user_permissions = get_user_permissions(user)

        if (user.is_staff or user.is_superuser):
            is_permited = True
        for permission in user_permissions:
            if required_permission in permission:
                is_permited = True
        all_fields = list(filter(lambda x: '.' in x, user_permissions))
        unparesd_fields = list(filter(lambda x: action in x, all_fields))
        parsed_fields = []
        for i in unparesd_fields:
            parsed_field = convert_to_fieldname(action, i)
            parsed_fields.append(parsed_field)

        if (len(parsed_fields) > 0):
            fields = parsed_fields
        if (required_permission in user_permissions):
            fields = None

        is_allowed = user.is_email_verified and user.is_role_verified and is_permited
        if (not is_allowed):
            message += ', You are not permitted to ' + action + ' ' + modelname
        # new_track.prescriptions.set(model.symptoms.all())

        if (not user.is_role_verified):
            message += ', please waite staff to verify your role'
        if (not user.is_email_verified):
            message += ', please verfy your email'
        return {'is_premited': is_allowed, 'message': message, 'fields': fields}
    except:
        return {'is_premited': False, 'message': 'you are not authenticated'}


# get_permission_id
def get_permission_id(name, Model):
    if "Can" not in name:
        print(Fore.BLUE + Back.RED + '============ name error ============')
    id = None
    content_type = ContentType.objects.get_for_model(Model)

    try:
        id = Permission.objects.get(name=name, content_type=content_type).id
    except:
        make_fields_permissions(Permission, ContentType, Model)
        try:
            id = Permission.objects.get(name=name, content_type=content_type).id
        except:
            pass
    return id
