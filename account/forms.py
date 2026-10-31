from django import forms
from django.core.exceptions import ValidationError
from patients.models import Appointment, Service, SubService
from doctor.models import Doctor
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
from django.apps import apps



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'service', 'sub_service']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'sub_service': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'appointment-date'
                }
            ),
            'appointment_time': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'appointment-time',
            }),
        }

    # dito need dapat ma-align ung date and time sa flatpickr
    # base sa kung ano ung nasa javascript na flatpickr
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)  # Get profile from kwargs
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].input_formats = ['%I:%M %p']  # Matches Flatpickr's "h:i K" format

        # Add price display for service field
        self.fields['service'].label_from_instance = lambda obj: f"{obj.name} (₱{obj.price})"

        # Add price display for sub_service field
        self.fields['sub_service'].label_from_instance = lambda obj: f"{obj.SubService} (₱{obj.price})"

        # Make service and sub_service required
        self.fields['service'].required = True
        self.fields['sub_service'].required = True

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        sub_service = cleaned_data.get('sub_service')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        doctor = cleaned_data.get('doctor')

        if not service:
            self.add_error('service', 'Please select a service')
            return cleaned_data
        if not sub_service:
            self.add_error('sub_service', 'Please select a sub-service')
            return cleaned_data

        # Check for time slot conflicts
        if appointment_date and appointment_time:
            try:
                # Get the model class dynamically to avoid linter issues
                AppointmentModel = apps.get_model('patients', 'Appointment')
                
                # Query for existing appointments at the same date and time, regardless of doctor
                existing_appointments = AppointmentModel._default_manager.filter(
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=['pending', 'confirm', 'completed']  # Check all active appointments
                )

                # If this is an edit of an existing appointment, exclude it from the check
                if self.instance and self.instance.pk:
                    existing_appointments = existing_appointments.exclude(pk=self.instance.pk)

                if existing_appointments.exists():
                    existing_appt = existing_appointments.first()
                    status_display = existing_appt.get_status_display()
                    self.add_error('appointment_time', 
                        f'This time slot is already booked for {appointment_date} at {appointment_time}. '
                        f'There is a {status_display.lower()} appointment at this time. '
                        'Please choose a different time.'
                    )

            except Exception as e:
                print(f"Error in time slot validation: {str(e)}")
                import traceback
                print(traceback.format_exc())

        # Check for same service on same day (excluding cancelled appointments)
        if service and appointment_date and self.profile:
            try:
                # Query for existing appointments with same service and date
                existing_service_appointments = AppointmentModel._default_manager.filter(
                    profile=self.profile,
                    appointment_date=appointment_date,
                    service=service,
                    status__in=['pending', 'confirm', 'completed']  # Exclude cancelled appointments
                )

                if self.instance and self.instance.pk:
                    existing_service_appointments = existing_service_appointments.exclude(pk=self.instance.pk)

                if existing_service_appointments.exists():
                    # Get the status of the existing appointment
                    existing_appointment = existing_service_appointments.first()
                    status_message = "pending" if existing_appointment.status == 'pending' else \
                                   "confirmed" if existing_appointment.status == 'confirm' else \
                                   "completed"
                    
                    self.add_error('service', 
                        f'You already have a {status_message} appointment for {service.name} on {appointment_date}. '
                        'Please choose a different service or date.'
                    )
            except Exception as e:
                print(f"Error in service validation: {str(e)}")
                import traceback
                print(traceback.format_exc())

        return cleaned_data

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time and appointment_time.minute != 0:
            raise ValidationError("Appointment time must be on the hour (e.g., 10:00, 11:00).")
        return appointment_time

class RegisterForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-name',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name',
            'class': 'form-group'
        })
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-username',
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'class': 'form-group'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id': 'register-email',
            'placeholder': 'Enter your email',
            'autocomplete': 'username',
            'class': 'form-group'
        })
    )
    age = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'id': 'register-age',
            'placeholder': 'Enter your age',
            'class': 'form-group'
        })
    )
    contact = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-contact',
            'placeholder': 'Enter your contact number',
            'class': 'form-group'
        })
    )
    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'id': 'register-birthday',
            'placeholder': 'YYYY-MM-DD',
            'type': 'date',
            'class': 'form-group'
        })
    )
    gender = forms.ChoiceField(
        required=True,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={
            'id': 'register-gender',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'register-password',
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
            'class': 'form-group'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'register-confirm-password',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
            'class': 'form-group'
        })

    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 7:
            raise ValidationError('Password must be at least 7 characters long.')
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email