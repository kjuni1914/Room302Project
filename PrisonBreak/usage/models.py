from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.date} {self.start_time}-{self.end_time}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class Seat(models.Model):
    seat_number = models.IntegerField(unique=True)
    is_used = models.BooleanField(default=False)