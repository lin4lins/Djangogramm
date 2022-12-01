from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"email:{self.email}"

    users = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []