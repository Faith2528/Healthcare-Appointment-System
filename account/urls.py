from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView,clinicadmin

urlpatterns = [
    path('',views.homepage,name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment_policy/', views.appointment_policy, name='appointment_policy'),
    path('appointment-form/', views.appointment_form, name='appointment_form'),
    path('profile/', views.profile, name='profile'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('get-sub-services/', views.get_sub_services, name='get_sub_services'),
    path('clinic-admin',clinicadmin.as_view(),name = 'clinic_admin'),
    path('appointments/<str:status>/', views.appointment_status_view, name='appointment_status'),
    path('appointments/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('check-appointment-availability/', views.check_appointment_availability, name='check_appointment_availability'),
    path('appointments/<int:appointment_id>/follow-up/', views.send_followup_email, name='send_followup_email'),
]