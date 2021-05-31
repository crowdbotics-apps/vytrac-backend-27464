from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import Group
from django.db import models
from users.models import User
from calendars.models import Date


class Notifications(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    description = models.TextField(max_length=999, blank=True, null=True)
    deadline = models.DateTimeField(null=True)
    response_time = models.DurationField(null=True, blank=True)
    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),
    )
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    target_users = models.ManyToManyField(
        User, related_name='Notification_target_user', null=True, blank=True)
    target_groups = models.ManyToManyField(
        Group, related_name='Notification_target_groups', null=True, blank=True)


@receiver(signals.post_save, sender=Date)
def __init__(instance, sender, signal, *args, **kwargs):
    new_notifcations = Notifications.objects.create(
        title='date', priority='averge')
    new_notifcations.target_users.add(User.objects.get(id=1))


# TODO # new_notifcations.target_users.add(instance.users)
    # TODO A3
    # sender
    # if Profile.care_taker change => Notifications.target=Profile.care_taker
    # if  instance.change_message ='bla bla b'
    # notifcations = Notifications.create()
    # notifcations.target_users.set([user.id,user2.id])
    # notifcations.target_groups.set([group.id,group2.id])
