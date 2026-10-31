from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import JsonResponse
from django.contrib import messages
from patients.models import Appointment, Service, SubService, Patient, AppointmentStatusLog
from doctor.models import Doctor
from datetime import datetime
from .forms import AppointmentForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_superuser:
            return redirect('/admin/')
        elif user.is_staff:
            return redirect('/clinic-admin')
        return redirect('dashboard')



class clinicadmin(ListView):
    model = Appointment
    template_name = 'clinic_admin.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()

        context.update({
            'total_patients': Patient.objects.count(),
            'todays_appointments': Appointment.objects.filter(appointment_date=today).count(),
            'pending_count': Appointment.objects.filter(status='pending').count(),
            'confirmed_count': Appointment.objects.filter(status='confirm').count(),
            'completed_count': Appointment.objects.filter(status='completed').count(),
            'no_show_count': Appointment.objects.filter(status='no-show').count(),
        })
        return context


def homepage(request):
    return render(
        request,
        'home.html'
    )

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            age = form.cleaned_data['age']
            contact = form.cleaned_data['contact']
            birthday = form.cleaned_data['birthday']
            gender = form.cleaned_data['gender']

            # Create user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=name  # or split and use first_name, last_name
            )

            # Create profile linked to the user
            Profile.objects.create(
                user=user,
                phone=contact,
                gender=gender,
                age=age,
                date_of_birth=birthday,
                status_profile='patient'  # or change if you allow selecting status
            )

            return redirect('login')  # or wherever you want to redirect
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'patient_dashboard.html')
    else:
        return redirect('login')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    doctors = Doctor.objects.all()  # Get all doctors

    return render(request, 'patient_dashboard.html',
                  {
                      'username': request.user.username
                        ,'Profile': profile
                        ,'doctors': doctors
                  })

@login_required
def appointment(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    appointments = Appointment.objects.filter(profile=profile)

    for appointment in appointments:
        appointment.total_price = 0
        if appointment.service:
            appointment.total_price += appointment.service.price
        if appointment.sub_service:
            appointment.total_price += appointment.sub_service.price


    return render(request, 'appointment/appointment_records.html', {
        'username': request.user.username,
        'Profile': profile,
        'appointments': appointments,
    })


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle profile picture update if 'avatarInput' is present in FILES
        if request.FILES.get('avatarInput'):
            profile.image = request.FILES['avatarInput']
            profile.save()
            messages.success(request, 'Profile picture updated successfully!')
            return render(
                request,
                'patient_profile.html',
                {
                    'username': request.user.username,
                    'Profile': profile,
                }
            )
        
        # Handle contact number update
        if 'action' in request.POST and request.POST['action'] == 'update_contact':
            new_contact = request.POST.get('newContact')
            if new_contact:
                profile.phone = new_contact
                profile.save()
                return JsonResponse({
                    'success': True,
                    'new_contact': new_contact
                })
            return JsonResponse({
                'success': False,
                'error': 'Invalid contact number'
            })

        # Handle email update
        if 'action' in request.POST and request.POST['action'] == 'update_email':
            new_email = request.POST.get('newEmail')
            if new_email:
                request.user.email = new_email
                request.user.save()
                return JsonResponse({
                    'success': True,
                    'new_email': new_email
                })
            return JsonResponse({
                'success': False,
                'error': 'Invalid email address'
            })

    # This block handles GET requests
    return render(
        request,
        'patient_profile.html',
        {
            'username': request.user.username,
            'Profile': profile,
        }
    )

@login_required
def appointment_form(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    patient, created = Patient.objects.get_or_create(profile=profile)  # Ensure patient exists

    # Get doctor_id from the URL query parameters
    doctor_id = request.GET.get('doctor_id')
    doctor = None
    if doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)  # Retrieve the doctor instance

    if request.method == 'POST':
        form = AppointmentForm(request.POST, profile=profile)  # Pass profile here
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.profile = profile
            appointment.patient = patient  # Assign the patient here
            appointment.doctor = doctor  # Automatically set the doctor
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment')
    else:
        # Pre-fill the doctor field in the form
        form = AppointmentForm(initial={'doctor': doctor}, profile=profile)  # Pass profile here too

    return render(request, 'appointment/appointment_form.html', {
        'form': form,
        'Profile': profile,
        'username': request.user.username,
    })


def get_appointment_details(request):
    appointment_id = request.GET.get('appointment_id')
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        data = {
            'date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'time': appointment.appointment_date.strftime('%H:%M'),
            'doctor': str(appointment.doctor),
            'service': str(appointment.service.name) if appointment.service else 'N/A',
            'service_price': appointment.service.price if appointment.service else 0,
            'sub_service': str(appointment.sub_service.SubService) if appointment.sub_service else 'N/A',
            'sub_service_price': appointment.sub_service.price if appointment.sub_service else 0,
        }
        return JsonResponse(data)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    

@login_required
def available_slots(request):
    date = request.GET.get('date')
    # Your logic to get available slots for the date
    # Example response:
    slots = [
        {
            'doctor_id': 1,
            'doctor_name': 'Dr. Smith',
            'time': '10:00',
            'datetime': f'{date}T10:00'
        },
        # ... more slots ...
    ]
    return JsonResponse({'slots': slots})

def get_sub_services(request):
    service_id = request.GET.get('service_id')
    sub_services = SubService.objects.filter(service_id=service_id).values('id', 'SubService', 'price')
    return JsonResponse(list(sub_services), safe=False)

@login_required
def appointment_status_view(request, status):
    template_map = {
        'confirm': 'confirm.html',
        'pending': 'pending.html',
        'completed': 'completed.html',
        'no-show': 'no_show.html',
    }

    template_name = template_map.get(status)
    if not template_name:
        return render(request, 'appointments/404.html', status=404)

    appointments = Appointment.objects.filter(status=status)

    historical_confirmed = None
    if status == "confirm":
        past_ids = AppointmentStatusLog.objects.filter(old_status="confirm") \
            .values_list("appointment_id", flat=True)
        historical_confirmed = Appointment.objects.filter(id__in=past_ids).exclude(status="confirm")

    query = request.GET.get('q')
    if query:
        appointments = appointments.filter(
            Q(patient__profile__user__first_name__icontains=query) |
            Q(patient__profile__user__last_name__icontains=query) |
            Q(patient__profile__user__email__icontains=query) |
            Q(doctor__profile__user__first_name__icontains=query) |
            Q(doctor__profile__user__last_name__icontains=query)
        )

    context = {
        'appointments': appointments,
        'status': status,
        'historical_confirmed': historical_confirmed if historical_confirmed else [],
    }

    return render(request, template_name, context)

@login_required
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        # Handle JSON request for cancellation
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
            new_status = data.get("status")
            reason = data.get("reason")
            next_page = data.get("next_status_page", "confirm")
        else:
            # Handle form data request
            new_status = request.POST.get("status")
            reason = None
            next_page = request.POST.get("next_status_page", "confirm")

        valid_transitions = ["confirm", "completed", "no-show", "cancelled"]

        if new_status in valid_transitions and new_status != appointment.status:
            # Log the change for audit/history
            AppointmentStatusLog.objects.create(
                appointment=appointment,
                old_status=appointment.status,
                new_status=new_status,
                changed_by=request.user
            )

            # Apply the new status
            appointment.status = new_status
            appointment.save()

            # Get users
            patient_user = appointment.patient.profile.user
            doctor_user = appointment.doctor.profile.user

            patient_email = patient_user.email
            patient_name = patient_user.get_full_name() or patient_user.username
            doctor_name = doctor_user.get_full_name() or doctor_user.username

            appointment_date = appointment.appointment_date
            appointment_time = appointment.appointment_time.strftime('%I:%M %p')

            if new_status == "confirm":
                subject = "Your Appointment Has Been Confirmed"
                message = (
                    f"Dear {patient_name},\n\n"
                    f"Your appointment with Dr. {doctor_name} on {appointment_date} at {appointment_time} "
                    f"has been confirmed.\n\nThank you!"
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])

            elif new_status == "completed":
                subject = "Your Appointment Has Been Completed"
                message = (
                    f"Dear {patient_name},\n\n"
                    f"Your appointment with Dr. {doctor_name} on {appointment_date} at {appointment_time} "
                    f"has been marked as completed.\n\nThank you!"
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])
                
            elif new_status == "no-show":
                subject = "You Have Missed Your Appointment"
                message = (
                    f"Dear {patient_name},\n\n"
                    f"You have missed your appointment with Dr. {doctor_name} that was set to take place in {appointment_date} at {appointment_time}. "
                    f"Please contact us if you wish to follow-up with your appointment.\n\nThank you!"
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])
                
            elif new_status == "cancelled":
                subject = "Your Appointment Has Been Cancelled"
                message = (
                    f"Dear {patient_name},\n\n"
                    f"Your appointment with Dr. {doctor_name} scheduled for {appointment_date} at {appointment_time} "
                    f"has been cancelled.\n\n"
                )
                
                if reason:
                    message += f"Reason for cancellation: {reason}\n\n"
                
                message += "If you have any questions or would like to reschedule, please contact our clinic at 09171234567 or email us at ledentalclinic0101@gmail.com.\n\nThank you!"
                
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])

            if request.content_type == 'application/json':
                return JsonResponse({'success': True})
            return redirect("appointment_status", status=next_page)

    if request.content_type == 'application/json':
        return JsonResponse({'success': False}, status=400)
    return redirect("appointment_status", status="confirm")

@login_required
def appointment_policy(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'appointment_policy.html', {
        'username': request.user.username,
        'Profile': profile,
    })

@login_required
def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id, profile=request.user.profile)
        appointment.status = 'cancelled'
        appointment.save()
        
        # Log the status change
        AppointmentStatusLog.objects.create(
            appointment=appointment,
            old_status=appointment.status,
            new_status='cancelled',
            changed_by=request.user
        )
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def check_appointment_availability(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        time = request.GET.get('time')
        doctor_id = request.GET.get('doctor')

        if not all([date, time, doctor_id]):
            return JsonResponse({'available': False, 'error': 'Missing required parameters'})

        try:
            # Convert string inputs to proper datetime objects
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time, '%I:%M %p').time()

            # Check for existing appointments at the same date and time
            existing_appointments = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                doctor_id=doctor_id,
                status__in=['pending', 'confirm']
            )

            available = not existing_appointments.exists()
            return JsonResponse({
                'available': available,
                'message': 'This time slot is already booked.' if not available else ''
            })

        except Exception as e:
            return JsonResponse({'available': False, 'error': str(e)})

    return JsonResponse({'available': False, 'error': 'Invalid request method'})

@login_required
def send_followup_email(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        # Get patient details
        patient_user = appointment.patient.profile.user
        patient_email = patient_user.email
        patient_name = patient_user.get_full_name() or patient_user.username

        # Send follow-up email
        subject = "Follow-up for Missed Appointment"
        message = (
            f"Dear {patient_name},\n\n"
            f"We want to reconfirm whether or not you want to follow up with your missed appointment. "
            f"If you wish to do so, please contact our clinic at 09171234567 or email us at ledentalclinic0101@gmail.com.\n\n"
            f"Thank you!"
        )
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


