// Sidebar toggle logic
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
}

// Sidebar active link logic
document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', function(e) {
        document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// Logout function
function logout() {
    window.location.href = "login.html";
}

// Doctor dropdown logic
function toggleDoctorDropdown(event, btn) {
    event.stopPropagation();
    document.querySelectorAll('.doctor-dropdown-menu').forEach(menu => {
        if (menu !== btn.nextElementSibling) {
            menu.style.display = 'none';
        }
    });
    const menu = btn.nextElementSibling;
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

// Show submenu when clicking anywhere on doctor-info except the dropdown button
document.querySelectorAll('.doctor-info').forEach(info => {
    info.addEventListener('click', function(e) {
        if (e.target.classList.contains('doctor-dropdown-btn')) return;
        document.querySelectorAll('.doctor-dropdown-menu').forEach(menu => {
            if (menu !== this.querySelector('.doctor-dropdown-menu')) {
                menu.style.display = 'none';
            }
        });
        const menu = this.querySelector('.doctor-dropdown-menu');
        menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
        e.stopPropagation();
    });
});

// Close dropdown when clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.doctor-dropdown-menu').forEach(menu => menu.style.display = 'none');
});

// Example functions for dropdown actions
function viewProfile(doctorName) {
    alert('Viewing profile for ' + doctorName);
}
function setAppointment(doctorName) {
    // Encode the doctor's name for the URL
    const url = `appointment_form.html?doctor=${encodeURIComponent(doctorName)}`;
    window.location.href = url;
}

// Appointment form submission
const appointmentForm = document.getElementById('appointmentForm');
if (appointmentForm) {
    appointmentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Your appointment request has been submitted!');
    });
}
 flatpickr("#appointment-time", {
  enableTime: true,
  noCalendar: true,
  dateFormat: "h:i K",       // 12-hour format with AM/PM
  time_24hr: false,
  minuteIncrement: 60,
  minTime: "09:00",
  maxTime: "18:00",
  defaultHour: 9
});

document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('appointment-date');
    const today = new Date().toISOString().split('T')[0]; // Format: YYYY-MM-DD
    dateInput.setAttribute('min', today);
});


// Patient Profile Picture Dropdown & Change Logic
const cameraBtn = document.getElementById('cameraBtn');
const avatarDropdown = document.getElementById('avatarDropdown');
const avatarInput = document.getElementById('avatarInput');
const patientAvatar = document.getElementById('patientAvatar');
const navbarAvatar = document.getElementById('navbarAvatar');

if (cameraBtn && avatarDropdown) {
    document.addEventListener('click', function(e) {
        if (cameraBtn.contains(e.target)) {
            avatarDropdown.style.display = avatarDropdown.style.display === 'block' ? 'none' : 'block';
        } else if (!avatarDropdown.contains(e.target)) {
            avatarDropdown.style.display = 'none';
        }
    });
}

if (avatarInput && patientAvatar && navbarAvatar) {
    avatarInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(evt) {
                patientAvatar.src = evt.target.result;
                navbarAvatar.src = evt.target.result;
                avatarDropdown.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });
}

// Auto-select doctor in appointment form if passed via URL and lock selection
document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const doctor = params.get('doctor');
    const doctorInput = document.getElementById('doctorName');
    const lockMsg = document.getElementById('doctorLockedMsg');
    if (doctor && doctorInput) {
        doctorInput.value = doctor;
        doctorInput.readOnly = true;
        if (lockMsg) lockMsg.style.display = 'inline';
    }
});

// Show modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}
// Hide modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Attach to buttons
function changeUsername() {
    openModal('changeUsernameModal');
}
function changePassword() {
    openModal('changePasswordModal');
}

// Example form handlers (replace with real logic)
document.addEventListener('DOMContentLoaded', function() {
    // Change Username Modal Form Handler
    document.getElementById('changeUsernameForm').onsubmit = function(e) {
        e.preventDefault();
        const newUsername = document.getElementById('newUsername').value;
        // Update the username in the profile section
        const usernameSpan = document.getElementById('usernameValue');
        if (usernameSpan) {
            usernameSpan.textContent = newUsername;
        }
        // Update the patient name heading if you want it to reflect the username
        const patientNameHeading = document.querySelector('.patient-name');
        if (patientNameHeading) {
            patientNameHeading.textContent = newUsername;
        }
        closeModal('changeUsernameModal');
    };

    // Change Password Modal Form Handler
    document.getElementById('changePasswordForm').onsubmit = function(e) {
        e.preventDefault();
        alert('Password changed!');
        closeModal('changePasswordModal');
    };

    // Change Contact Number Modal Form Handler
    const changeContactForm = document.getElementById('changeContactForm');
    if (changeContactForm) {
        changeContactForm.onsubmit = function(e) {
            e.preventDefault();
            const newContact = document.getElementById('newContact').value;
            const contactSpan = document.getElementById('contactValue');
            if (contactSpan) {
                contactSpan.textContent = newContact;
            }
            closeModal('changeContactModal');
        };
    }

    // Change Email Modal Form Handler
    const changeEmailForm = document.getElementById('changeEmailForm');
    if (changeEmailForm) {
        changeEmailForm.onsubmit = function(e) {
            e.preventDefault();
            const newEmail = document.getElementById('newEmail').value;
            const emailSpan = document.getElementById('emailValue');
            if (emailSpan) {
                emailSpan.textContent = newEmail;
            }
            closeModal('changeEmailModal');
        };
    }
});



document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('id_service');
    const subServiceSelect = document.getElementById('id_sub_service');

    // Reset sub-service dropdown
    function resetSubServiceSelect(message = 'Select a sub-service') {
        subServiceSelect.innerHTML = `<option value="">${message}</option>`;
        subServiceSelect.disabled = true;
    }

    serviceSelect.addEventListener('change', function() {
        const serviceId = this.value;

        if (serviceId) {
            fetch(`/get-sub-services/?service_id=${serviceId}`)
                .then(response => response.json())
                .then(data => {
                    resetSubServiceSelect();
data.forEach(sub => {
    const option = document.createElement('option');
    option.value = sub.id;
    option.textContent = `${sub.SubService} (₱${sub.price})`;
    subServiceSelect.appendChild(option);
});

                    subServiceSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Error fetching sub-services:', error);
                    resetSubServiceSelect('Error loading sub-services');
                });
        } else {
            resetSubServiceSelect();
        }
    });

    // Trigger initial reset
    resetSubServiceSelect('Select a service first');
});



  function toggleHistory() {
    const section = document.getElementById("historical-confirmed");
    const label = document.getElementById("history-toggle-label");

    const isHidden = section.style.display === "none";

    section.style.display = isHidden ? "" : "none";
    label.textContent = isHidden
      ? "Hide previously confirmed appointments ▲"
      : "Show previously confirmed appointments ▼";
  }

function checkAppointmentAvailability() {
    const dateInput = document.getElementById('appointment-date');
    const timeInput = document.getElementById('appointment-time');
    const doctorSelect = document.getElementById('id_doctor');
    const submitButton = document.querySelector('button[type="submit"]');

    if (!dateInput || !timeInput || !doctorSelect || !submitButton) {
        return; // Required elements not found
    }

    const date = dateInput.value;
    const time = timeInput.value;
    const doctorId = doctorSelect.value;

    if (!date || !time || !doctorId) {
        return; // Missing required values
    }

    // Make AJAX request to check availability
    fetch(`/check-appointment-availability/?date=${date}&time=${time}&doctor=${doctorId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.available) {
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger';
                errorDiv.textContent = data.message || 'This time slot is not available.';
                
                // Remove any existing error messages
                const existingError = document.querySelector('.alert-danger');
                if (existingError) {
                    existingError.remove();
                }
                
                // Insert error message before the form
                const form = document.querySelector('form');
                form.parentNode.insertBefore(errorDiv, form);
                
                // Disable submit button
                submitButton.disabled = true;
            } else {
                // Remove error message if exists
                const existingError = document.querySelector('.alert-danger');
                if (existingError) {
                    existingError.remove();
                }
                
                // Enable submit button
                submitButton.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error checking appointment availability:', error);
        });
}

// Add event listeners for date and time inputs
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('appointment-date');
    const timeInput = document.getElementById('appointment-time');
    const doctorSelect = document.getElementById('id_doctor');

    if (dateInput && timeInput && doctorSelect) {
        dateInput.addEventListener('change', checkAppointmentAvailability);
        timeInput.addEventListener('change', checkAppointmentAvailability);
        doctorSelect.addEventListener('change', checkAppointmentAvailability);
    }
});
