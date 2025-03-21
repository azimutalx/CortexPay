from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('atacadista', 'Atacadista'),
        ('varejista', 'Varejista'),
        ('cliente', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    name = models.CharField(max_length=100, blank=True)