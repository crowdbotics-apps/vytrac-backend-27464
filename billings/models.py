from django.db import models
from users.models import User
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel, NO_DELETE


class CPTcode(SafeDeleteModel):
    code = models.CharField(max_length=30, unique=True)


class Payment(SafeDeleteModel):
    qualified_CPTs = models.ManyToManyField(
        CPTcode, related_name='who_can_see_comment', blank=True)
    # or
    # qualified_CPTs = models.OneToOneField(
    #         CPTcode,
    #         null=True,
    #         blank=True,
    #         on_delete=models.CASCADE,
    #         primary_key=False,
    #     )
    eligible = models.BooleanField(default=False)
    report_generated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_payed = models.BooleanField(default=False)
    amount = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, related_name='Payment_user',
                             on_delete=models.DO_NOTHING, null=True,)
