import logging
# from coleman.utils.mail import send_mail_async as send_mail
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(
        _("last modified"), auto_now=True, editable=False)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return "[%s] %s" % (self.number, self.title)

    @property
    def number(self):
        return "{:08d}".format(self.pk)

    def get_tasks_viewer_url(self):
        """
        Verification token added to the Taskss Viewer URL so each one
        sent through email cannot be used to change the order number and
        access to other orders.
        It uses as input a salt code configured and the ID number.
        See: coleman/settings_emails.py
             https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer
        """
        salt = settings.TASKS_VIEWER_HASH_SALT
        if not settings.DEBUG and salt == '1two3':
            logger.warning(
                "Insecure salt code used to send email orders, do NOT use it in PRODUCTION")
        # created_at_as_iso = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # This ISO format is the same used
            # used by the REST serializer
        # SHA-1 is enough secure for
        token = "{}-{}".format(salt, self.pk)
        # this purpose (SHA-2 is too long)
        token = sha1(token.encode('utf-8')).hexdigest()
        return settings.TASKS_VIEWER_ENDPOINT.format(number=self.number, token=token)


#     def save(self, *args, **kwargs):
#         task_created = self.pk is None
#         super().save(*args, **kwargs)
#         if task_created:
#             self.send_new_task_email()

#     def send_new_task_email(self):
#         emails_to = []
#         if settings.TASKS_SEND_EMAILS_TO_PARTNERS and getattr(self, "user", None) and self.user.email:
#             emails_to.append(self.user.email)
#         if settings.TASKS_SEND_EMAILS_TO_ASSIGNED and getattr(self, "user", None) and self.user.email:
#             emails_to.append(self.user.email)
#         if len(emails_to):
#             logger.info(
#                 "[Tasks #%s] Sending task creation email to: %s", self.number, emails_to)
#             vals = {
#                 "id": self.number,
#                 "user": str(self.user) if getattr(self, "user", None) else '(Not assigned yet)',
#                 "title": self.title,
#                 "description": self.description or '-',
#                 "sign": settings.SITE_HEADER,
#             }
#             if settings.TASKS_VIEWER_ENABLED:
#                 email_template = settings.MTASKS_EMAIL_WITH_URL
#                 vals["url"] = self.get_tasks_viewer_url()
#             else:
#                 email_template = settings.MTASKS_EMAIL_WITHOUT_URL
        # try:
        #     send_mail(
        #         '[{app}] [#{id}] New Tasks Created'.format(
        #             app=settings.APP_NAME, id=self.number),
        #         email_template.format(**vals),
        #         settings.APP_EMAIL,
        #         emails_to,
        #     )
        # except Exception as e:
        #     logger.warning("[Tasks #%s] Error trying to send the task creation email - %s: %s",
        #                    self.number, e.__class__.__name__, str(e))
