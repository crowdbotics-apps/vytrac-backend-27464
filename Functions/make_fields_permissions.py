
from django.apps import AppConfig



def make_fields_permissions(Permission,ContentType,Model):
    mode_name = Model.__name__.lower()
    permissions = []
    for item in Model._meta.fields:
        permissions.append(('view_'+mode_name+'.'+item.name+'_field',
                            'Can view '+item.name.replace('_', ' ')))

    for item in Model._meta.fields:
        permissions.append(('change_'+mode_name+'.'+item.name+'_field',
                            'Can change '+item.name.replace('_', ' ')))
    for codename, permission_name in permissions:
        Permission.objects.get_or_create(
                codename=codename,
                name=permission_name,
                content_type=ContentType.objects.get_for_model(Model),
            )
#


from django.db import models


class YourAppConfig(AppConfig):

    default_auto_field = 'django.db.models.AutoField'  # Don't modify, keep it as it is in your code
    name = 'Functions.make_fields_permissions'  # Don't modify, keep it as it is in your code

    def ready(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from django import apps
        # class Alert(models.Model):
        #     pass
        # Permission.objects.get_or_create(
        #     codename='view_alert',
        #     name="Can view alert",
        #     content_type=ContentType.objects.get_for_model(Alert)
        # )
        # for Model in apps.apps.get_models():
        #     make_fields_permissions(Permission, ContentType,Model)

