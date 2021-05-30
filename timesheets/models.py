
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField
from safedelete.models import SafeDeleteModel, NO_DELETE
from django.db.models import signals
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from manage_patients.models import Profile, Symptoms
from users.models import User
import ast
from calendars.models import DateType
import getpass


class ChangeTrack(SafeDeleteModel):
    # TODO automaticlly add the current loged in user
    by = models.ForeignKey(settings.AUTH_USER_MODEL,
                           null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    RCHOICES = (
        ('added', 'added'),
        ('changed', 'changed'),
        ('deleted', 'deleted'),
    )
    action_type = models.CharField(choices=RCHOICES, max_length=50, blank=True)
    related_to = models.ForeignKey(
        User, related_name='related_name', null=True, on_delete=models.SET_NULL)
    model_target = models.CharField(max_length=50, blank=True)
    object_id = models.IntegerField(max_length=50, blank=True, null=True)
    field_target = models.CharField(max_length=50, blank=True)
    field_value = models.CharField(max_length=50, blank=True)


@receiver(signals.pre_save, sender=Profile)
def __init__(instance, update_fields, sender, *args, **kwargs):
    try:
        old_object = Profile.objects.get(id=instance.id)
        for index, item in enumerate(old_object._meta.fields):
            field_target = item.name
            field_value = str(getattr(instance, field_target))
            old_field_value = str(getattr(old_object, field_target))
            # TODO symptoms
            # print('======================')
            # print(instance.symptoms.all())
            # print(old_object.symptoms.all())
            # print('======================')
            if (old_field_value != field_value):
                # TODO realted_to = Profile.user
                ChangeTrack.objects.create(action_type='changed', model_target=str(
                    'Profile'), field_value=field_value, field_target=field_target, object_id=instance.id)
    except:
        pass


@receiver(signals.post_save, sender=Profile)
def __init__(instance, created, update_fields, sender, *args, **kwargs):
    if (created):
        for index, item in enumerate(instance._meta.fields):
            field_target = item.name
            field_value = str(getattr(instance, field_target))
            # TODO realted_to = Profile.user
            ChangeTrack.objects.create(action_type='added', model_target=str(
                'DateType'), field_value=field_value, field_target=field_target, object_id=instance.id)


# @receiver(signals.pre_delete,sender=DateType)
# def __init__(instance,created,sender, *args, **kwargs):
#     ChangeTrack.objects.create(action_type='delete',model_target=str('DateType'))
#     # sender_object = sender.objects.get(id=instance.id)
#     # try:
#         # obj = instance.change_message
#         # obj = ast.literal_eval(obj)

#     #     for field in obj:
#     #         for key in field.keys():
#     #             print('x ================')
#     #             print(key)
#     #             for field2 in field[key]['fields']:
#     #                 print(instance[field2])
#     #                 print(sender_object[key])
#     #                 print(sender_object['name'])

#     #                 print({'with dont':sender_object.name})


#     #                 print(field2)
#     # except:
#     #     print('error ================')
#     # print(instance)


# # # @receiver(signals.post_delete)
# # # def __init__(self, *args, **kwargs):
# # #     try:
# # #         # obj = instance.change_message
# # #         # obj = ast.literal_eval(obj)
# # #         print(self)
# # #     except:
# # #         print('error ================')
# # #     # print(instance)
