from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Creator)
admin.site.register(models.Release)
admin.site.register(models.Rating)
admin.site.register(models.Review)
