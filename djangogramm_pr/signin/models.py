from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    # fields to fill after email confirmation
    full_name = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=255, null=True)
    avatar_path = models.ImageField(upload_to="avatars", null=True)

    def __str__(self):
        return f"email:{self.email}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []