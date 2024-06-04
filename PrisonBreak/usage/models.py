"""
models.py

This file contains the data models for the seating reservation application.
"""

from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    """
    Reservation model representing a user's seat reservation.

    Attributes:
        user (ForeignKey): A foreign key linking to the User who made the reservation.
        date (DateField): The date of the reservation.
        start_time (TimeField): The start time of the reservation.
        end_time (TimeField): The end time of the reservation.
        is_confirmed (BooleanField): Status indicating if the reservation is confirmed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.date} {self.start_time}-{self.end_time}"

class UserProfile(models.Model):
    """
    UserProfile model representing additional information about the user.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        security_question (CharField): The security question for account recovery.
        security_answer (CharField): The answer to the security question.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Seat(models.Model):
    """
    Seat model representing each seat in the system.

    Attributes:
        seat_number (IntegerField): The number assigned to the seat.
        is_used (BooleanField): Status indicating if the seat is currently in use.
        user (ForeignKey): A foreign key linking to the User currently occupying the seat.
        start_time (DateTimeField): The start time of the seat usage.
        expected_duration (IntegerField): The expected duration of the seat usage in minutes.
    """
    seat_number = models.IntegerField(unique=True)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(null=True, blank=True)
    expected_duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Seat {self.seat_number}'
