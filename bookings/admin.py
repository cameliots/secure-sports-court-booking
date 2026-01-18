from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'court',
        'booking_date',
        'booking_time',
        'created_at',
    )

    list_filter = (
        'booking_date',
        'court',
    )

    search_fields = (
        'user__username',
        'court__name',
    )

    ordering = (
        '-created_at',
    )
