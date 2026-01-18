from django import forms
from datetime import date, datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Booking, TIME_SLOTS
from courts.models import Court


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['court', 'booking_date', 'booking_time']
        widgets = {
            'court': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'booking_time': forms.Select(
                choices=TIME_SLOTS,
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.sport = kwargs.pop('sport', None)
        super().__init__(*args, **kwargs)

        self.fields['court'].empty_label = None

        if self.sport:
            queryset = Court.objects.filter(
                sport_type__iexact=self.sport,
                is_available=True
            )

            # Allow current court during edit
            if self.instance.pk and self.instance.court:
                queryset = queryset | Court.objects.filter(
                    pk=self.instance.court.pk
                )

            self.fields['court'].queryset = queryset.distinct()
        else:
            self.fields['court'].queryset = Court.objects.none()

    # ==========================
    # DATE VALIDATION
    # ==========================
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')

        if booking_date and booking_date < date.today():
            raise ValidationError(
                "Booking date cannot be in the past."
            )

        return booking_date

    # ==========================
    # FORM-LEVEL VALIDATION
    # ==========================
    def clean(self):
        cleaned_data = super().clean()

        court = cleaned_data.get('court')
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')

        # ==========================
        # ALLOW UNCHANGED EDITS
        # ==========================
        if self.instance.pk:
            if (
                booking_date == self.instance.booking_date and
                booking_time == self.instance.booking_time and
                court == self.instance.court
            ):
                return cleaned_data

        # ==========================
        # PREVENT PAST DATE + TIME
        # ==========================
        if booking_date and booking_time:
            try:
                # IMPORTANT: booking_time is a STRING like "21:00" or "21:00 – 22:00"
                start_time_str = booking_time.split("–")[0].strip()
                booking_time_obj = datetime.strptime(
                    start_time_str, "%H:%M"
                ).time()
            except Exception:
                raise ValidationError(
                    "Invalid booking time format."
                )

            booking_datetime = datetime.combine(
                booking_date,
                booking_time_obj
            )

            # Make timezone-aware
            booking_datetime = timezone.make_aware(booking_datetime)

            if booking_datetime <= timezone.now():
                raise ValidationError(
                    "You cannot create a booking for a past date or time."
                )

        # ==========================
        # PREVENT DUPLICATE BOOKINGS
        # ==========================
        if court and booking_date and booking_time:
            existing_booking = Booking.objects.filter(
                court=court,
                booking_date=booking_date,
                booking_time=booking_time
            )

            if self.instance.pk:
                existing_booking = existing_booking.exclude(
                    pk=self.instance.pk
                )

            if existing_booking.exists():
                raise ValidationError(
                    "This time slot is already booked."
                )

        return cleaned_data
