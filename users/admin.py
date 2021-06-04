from django.contrib import admin

#
from . import models

admin.site.register(models.User)
admin.site.register(models.Availablity)
admin.site.register(models.Settings)


# potnetially we may need to keep group named group.
# admin.site.register(models.User)
# admin.site.register(models.Other)
# admin.site.register(models.Other)
# admin.site.register(models.Other)
