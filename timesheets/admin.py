from django.contrib import admin
from . import models

admin.site.register(models.Column)
admin.site.register(models.Value)
# admin.site.register(models.Name)

