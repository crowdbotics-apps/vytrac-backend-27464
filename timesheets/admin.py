from django.contrib import admin

#
from . import models

admin.site.register(models.ChangeTrack)
admin.site.register(models.PatientProfileTracker)
