from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
import inspect

#
from . import models

admin.site.register(models.User)
admin.site.register(models.Availablity)

# potnetially we may need to keep group named group.
# admin.site.register(models.User)
# admin.site.register(models.Other)
# admin.site.register(models.Other)
# admin.site.register(models.Other)
