import logging
# from coleman.utils.mail import send_mail_async as send_mail
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from calendars.models import Event

logger = logging.getLogger(__name__)

number_tr = _("number")


class Tasks(models.Model):
    class Meta:
        verbose_name = _("Tasks")
        verbose_name_plural = _("Taskss")

    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )

    PRIORITIES = (
        ('00_low', _('Low')),
        ('10_normal', _('Normal')),
        ('20_high', _('High')),
        ('30_critical', _('Critical')),
        ('40_blocker', _('Blocker'))
    )
    TYPES = (
        ('daily_plan', _('Daily plan')),
        ('task', _('task')),
        ('emergency', _('Emergency')),
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(
        _("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(
        _("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateTimeField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20,
                             choices=STATUSES, default='to-do')
    priority = models.CharField(
        _("priority"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(
        _("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(
        _("last modified"), auto_now=True, editable=False)
    pations = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='pations_daily_plan', blank=True)

    responsible = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='responsible', blank=True)
    dates = models.ManyToManyField(
        Event, related_name='responsible', blank=True)
    type = models.CharField(
        _("type"), max_length=20, choices=TYPES, default='10_normal')

    def __str__(self):
        return "[%s] %s" % (self.number, self.title)

    class Meta:
        get_latest_by = 'date_created'

    @property
    def number(self):
        return "{:08d}".format(self.pk)