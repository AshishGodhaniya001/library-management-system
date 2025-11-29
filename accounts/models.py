from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    enrollment_no = models.CharField(max_length=50, blank=True, null=True)  # for students

    def __str__(self):
        return f"{self.username} ({self.role})"
