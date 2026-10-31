from django.contrib import admin
from .models import Doctor
from unfold.admin import ModelAdmin
# Register your models here.
@admin.register(Doctor)
class adminDoctor(ModelAdmin):
    pass
