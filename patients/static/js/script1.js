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

// Flatpickr calendar
if (typeof flatpickr !== "undefined" && document.getElementById('calendar-widget')) {
    const calendar = flatpickr("#calendar-widget", {
        inline: true,
        minDate: "today",
        onChange: function(selectedDates, dateStr, instance) {
            document.getElementById('appointmentDate').value = dateStr;
        }
    });

    const appointmentDate = document.getElementById('appointmentDate');
    if (appointmentDate) {
        appointmentDate.addEventListener('change', function() {
            calendar.setDate(this.value, true);
        });
    }
}

// Sub-service options logic
const subServices = {
    service_1: ["sub_one", "sub_two", "sub_three"],
    service_2: ["sub_one", "sub_two", "sub_three"],
    service_3: ["sub_one", "sub_two", "sub_three"]
};

const serviceType = document.getElementById('serviceType');
const subServiceType = document.getElementById('subServiceType');
if (serviceType && subServiceType) {
    serviceType.addEventListener('change', function() {
        subServiceType.innerHTML = '<option value="">Select a sub-service</option>';
        const selected = this.value;
        if (subServices[selected]) {
            subServices[selected].forEach(sub => {
                const opt = document.createElement('option');
                opt.value = sub;
                opt.textContent = sub;
                subServiceType.appendChild(opt);
            });
            subServiceType.disabled = false;
        } else {
            subServiceType.disabled = true;
        }
    });
}

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



