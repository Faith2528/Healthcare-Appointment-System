from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES  = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True,null=True,)
    address = models.TextField(blank=True,null=True,)
    image = models.ImageField(upload_to='images/',blank=True,null=True,)
    gender = models.CharField(blank=True, null=True, max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    status_profile = models.CharField(blank=True, null=True, max_length=10, choices=STATUS_CHOICES,default='patient')

    def __str__(self):
        return f"{self.user.username}"