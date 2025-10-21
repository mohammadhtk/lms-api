from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
  username = models.CharField(max_length=50, null=True, blank=True, unique=True)
  email = models.EmailField(unique=True)
  phone_number = PhoneNumberField()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']
  
  
  
  
  
  