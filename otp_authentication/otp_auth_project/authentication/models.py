from django.db import models

# Create your models here.

class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    otp_hash = models.CharField(max_length=20, blank=True, null=True)
