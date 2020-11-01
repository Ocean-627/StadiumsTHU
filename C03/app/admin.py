from django.contrib import admin

# Register your models here.
from app import models
admin.site.register(models.User)
admin.site.register(models.Manager)
admin.site.register(models.Stadium)
admin.site.register(models.Court)
admin.site.register(models.Duration)
admin.site.register(models.ReserveEvent)
