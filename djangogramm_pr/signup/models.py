from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    def __str__(self):
        return f"email:{self.email}"