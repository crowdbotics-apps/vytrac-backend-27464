from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_actions(name):
    actions = {}
    for x in Permission.objects.all():
        # Debugging(x.name)
        actions['action_name'] = 'action name'
        # Debugging(x.codename)
    return actions


class Automation(models.Model):
    tag_name = models.SlugField()
    if_item = models.CharField(choices=(
        ('user.change_username', 'user | change username'),), max_length=50, blank=True)
    if_ction = models.CharField(choices=(
        ('user.change_username', 'user | change username'),), max_length=50, blank=True)
    then_item = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    then_action = models.CharField(choices=(
        ('user.change_username', 'user | change username'),), max_length=50, blank=True)
    then_set_value = models.CharField(choices=(
        ('user.change_username', 'user | change username'),), max_length=50, blank=True)
#     tagged_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag_name

# @Receiver(signals.post_save)
# def __init__(instance, sender, signal, *args, **kwargs):
# patients.care_taker is changed => set care_taker.permissions.can_see_Profile =False
# if user.group changed => autoremove from care_takerlist

#     try:
#         print('1======================')
#         print(instance.title)
#         print(instance.description)
#         print(instance.target_user_id)
#         print('1======================')
#     except:
#         pass
#     try:
#         print('2======================')
#         print(instance.id)
#         print(instance.action_time)
#         print(instance.user_id)
#         print(instance.content_type_id)
#         print(instance.object_id)
#         print(instance.object_repr)
#         print(instance.action_flag)
#         print(instance.change_message)
#         print('2======================')
#     except:
#         pass
