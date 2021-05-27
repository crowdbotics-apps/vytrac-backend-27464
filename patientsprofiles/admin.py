from django.contrib import admin
from . import models
admin.site.register(models.DalyPlan)
admin.site.register(models.PatientProfile)
admin.site.register(models.Roster)
admin.site.register(models.Symptoms)
