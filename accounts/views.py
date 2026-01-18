import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.exceptions import BadRequest, PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import OneTimePassword
from .utils import generate_otp

security_logger = logging.getLogger("security")

# ==========================
# REGISTER
# ==========================
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            security_logger.info(f"User registered: {user.username}")
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


# ==========================
# LOGIN (2FA STEP 1)
# ==========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate OTP
            otp_code = generate_otp()

            # Store or update OTP
            OneTimePassword.objects.update_or_create(
                user=user,
                defaults={'code': otp_code}
            )

            # Send OTP (console email backend)
            send_mail(
                subject="Your Login OTP",
                message=(
                    f"Your one-time password (OTP) is: {otp_code}\n\n"
                    "This code will expire in 5 minutes."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

            # Save user ID temporarily in session
            request.session['otp_user_id'] = user.id

            security_logger.info(f"OTP generated for user: {user.username}")

            return redirect("verify_otp")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ==========================
# OTP VERIFICATION (2FA STEP 2)
# ==========================
def verify_otp(request):
    user_id = request.session.get("otp_user_id")

    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
        otp_obj = OneTimePassword.objects.get(user=user)
    except (User.DoesNotExist, OneTimePassword.DoesNotExist):
        messages.error(request, "OTP verification failed.")
        return redirect("login")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if otp_obj.code == entered_otp and not otp_obj.is_expired():
            login(request, user)

            # Cleanup
            otp_obj.delete()
            del request.session["otp_user_id"]

            security_logger.info(f"2FA login successful: {user.username}")
            return redirect("home")

        messages.error(request, "Invalid or expired OTP")

    return render(request, "accounts/verify_otp.html")


# ==========================
# PROFILE
# ==========================
@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            security_logger.info(f"Profile updated by {request.user.username}")
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


# ==========================
# CHANGE PASSWORD
# ==========================
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            security_logger.info(f"Password changed by {request.user.username}")
            messages.success(request, "Password updated successfully")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


# ==========================
# ERROR HANDLERS
# ==========================
def bad_request_view(request, exception=None):
    return render(request, "errors/400.html", status=400)

def permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", status=403)

def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=404)

def server_error_view(request):
    return render(request, "errors/500.html", status=500)


# ==========================
# TEST ROUTES
# ==========================
def test_400(request):
    raise BadRequest()

def test_403(request):
    raise PermissionDenied()

def test_500(request):
    raise Exception("Intentional server error")


# ==========================
# SECURITY LOGGING (SIGNALS)
# ==========================
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user.is_staff:
        security_logger.info(f"Admin login: {user.username}")
    else:
        security_logger.info(f"User login: {user.username}")

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get("username", "UNKNOWN")
    security_logger.warning(
        f"FAILED LOGIN – username={username} – time={timezone.now()}"
    )
