from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    last_request_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
