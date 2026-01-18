import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Booking
from .forms import BookingForm
from logs.models import AuditLog   # ✅ AUDIT LOG

# 🔐 Security file logger
security_logger = logging.getLogger('security')


# ==========================
# DASHBOARD
# ==========================
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ==========================
# CREATE BOOKING
# ==========================
@login_required
def create_booking(request):
    sport = request.GET.get('sport')

    if request.method == 'POST':
        form = BookingForm(request.POST, sport=sport)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            # 🔐 FILE SECURITY LOG
            security_logger.info(
                f"Booking CREATED | user={request.user.username} | "
                f"court={booking.court} | "
                f"date={booking.booking_date} | "
                f"time={booking.booking_time}"
            )

            # 🧾 AUDIT LOG (DATABASE)
            AuditLog.objects.create(
                user=request.user,
                action='BOOKING_CREATE',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, "Booking has been successfully created")
            return redirect('my_bookings')

    else:
        form = BookingForm(sport=sport)

    return render(
        request,
        'bookings/booking_form.html',
        {'form': form, 'sport': sport}
    )


# ==========================
# VIEW OWN BOOKINGS
# ==========================
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)

    return render(
        request,
        'bookings/booking_list.html',
        {'bookings': bookings}
    )


# ==========================
# UPDATE BOOKING
# ==========================
@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    sport = booking.court.sport_type if booking.court else None

    if request.method == 'POST':
        form = BookingForm(
            request.POST,
            instance=booking,
            sport=sport
        )

        if form.is_valid():
            form.save()

            # 🔐 FILE SECURITY LOG
            security_logger.info(
                f"Booking UPDATED | user={request.user.username} | booking_id={booking.id}"
            )

            # 🧾 AUDIT LOG
            AuditLog.objects.create(
                user=request.user,
                action='BOOKING_UPDATE',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, "Booking updated successfully")
            return redirect('my_bookings')

    else:
        form = BookingForm(instance=booking, sport=sport)

    return render(
        request,
        'bookings/booking_form.html',
        {'form': form}
    )


# ==========================
# DELETE BOOKING
# ==========================
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST':
        booking_id = booking.id
        booking.delete()

        # 🔐 FILE SECURITY LOG
        security_logger.info(
            f"Booking DELETED | user={request.user.username} | booking_id={booking_id}"
        )

        # 🧾 AUDIT LOG
        AuditLog.objects.create(
            user=request.user,
            action='BOOKING_DELETE',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        messages.success(request, "Booking deleted successfully")
        return redirect('my_bookings')

    return render(
        request,
        'bookings/booking_confirm_delete.html',
        {'booking': booking}
    )
