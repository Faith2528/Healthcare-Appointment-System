from django.db import models
from account.models import Profile

# Create your models here.
class Doctor(models.Model):
    StatusChoices = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default='Dentist')
    license_number = models.CharField(max_length=50)
    clinic_name = models.CharField(max_length=255, default="Dental Clinic")
    clinic_address = models.TextField()
    status = models.CharField(blank=True, null=True, max_length=11, choices=StatusChoices)


    def __str__(self):
        return f"Dr.{self.profile}"
