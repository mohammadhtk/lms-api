"""
User models for the application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel
from core.utils import generate_unique_code

# Custom user model with role-based access
class CustomUser(AbstractUser, TimeStampedModel):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
        ('receptionist', 'Receptionist'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def full_name(self):
        return self.get_full_name()

# Student profile model
class Student(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    student_code = models.CharField(max_length=20, unique=True, editable=False)
    current_level = models.CharField(max_length=10, blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)
    total_courses_taken = models.IntegerField(default=0)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.full_name} - {self.student_code}"

    def save(self, *args, **kwargs):
        if not self.student_code:
            self.student_code = generate_unique_code(prefix='STU', length=8)
        super().save(*args, **kwargs)

# Teacher profile model
class Teacher(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_code = models.CharField(max_length=20, unique=True, editable=False)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.user.full_name} - {self.specialization}"

    def save(self, *args, **kwargs):
        if not self.teacher_code:
            self.teacher_code = generate_unique_code(prefix='TCH', length=8)
        super().save(*args, **kwargs)
