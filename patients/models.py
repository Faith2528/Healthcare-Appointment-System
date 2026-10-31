from django.db import models
from account.models import Profile
from doctor.models import Doctor
import datetime

# Create your models here.
class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')

    def __str__(self):
        return f"{self.profile}"


class Appointment(models.Model):
    StatusChoices = (
        ('confirm', 'Confirm'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('no-show', 'No-Show'),
        ('cancelled', 'Cancelled'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments', default=1)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=datetime.time(9, 0))
    status = models.CharField(blank=True, null=True, max_length=10, choices=StatusChoices, default='pending')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='appointment_services', null=True, blank=True)  # Renamed field
    sub_service = models.ForeignKey('SubService', on_delete=models.CASCADE, related_name='appointment_sub_services', null=True, blank=True)

    def __str__(self):
        return f"{self.patient}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class SubService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='sub_service')
    SubService = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.SubService

class AppointmentStatusLog(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='status_logs')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment} changed from {self.old_status} to {self.new_status} on {self.changed_at}"



