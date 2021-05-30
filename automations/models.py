from django.db import models

# Create your models here.


# @receiver(signals.post_save)
# def __init__(instance, sender, signal, *args, **kwargs):
# Profile.care_taker is changed => set care_taker.permissions.can_see_Profile =False
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
