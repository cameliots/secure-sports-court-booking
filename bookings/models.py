from django.db import models
from django.contrib.auth.models import User
from courts.models import Court


# ==========================
# FIXED 1-HOUR TIME SLOTS
# ==========================
TIME_SLOTS = [
    ('08:00', '08:00 – 09:00'),
    ('09:00', '09:00 – 10:00'),
    ('10:00', '10:00 – 11:00'),
    ('11:00', '11:00 – 12:00'),
    ('12:00', '12:00 – 13:00'),
    ('13:00', '13:00 – 14:00'),
    ('14:00', '14:00 – 15:00'),
    ('15:00', '15:00 – 16:00'),
    ('16:00', '16:00 – 17:00'),
    ('17:00', '17:00 – 18:00'),
    ('18:00', '18:00 – 19:00'),
    ('19:00', '19:00 – 20:00'),
    ('20:00', '20:00 – 21:00'),
    ('21:00', '21:00 – 22:00'),
]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)

    booking_date = models.DateField()
    booking_time = models.CharField(
        max_length=5,
        choices=TIME_SLOTS
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 🔐 Prevent double booking
        constraints = [
            models.UniqueConstraint(
                fields=['court', 'booking_date', 'booking_time'],
                name='unique_court_booking'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - {self.court.name} "
            f"({self.booking_date} {self.booking_time})"
        )
