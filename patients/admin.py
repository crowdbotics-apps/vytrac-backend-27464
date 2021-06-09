from django.contrib import admin
from . import models
admin.site.register(models.Patient)
admin.site.register(models.Roster)
admin.site.register(models.Symptom)
admin.site.register(models.Reports)
admin.site.register(models.Conditions)
