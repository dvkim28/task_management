from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    position = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    about_info = models.TextField(blank=True, null=True)
