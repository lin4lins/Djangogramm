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


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    publication_date = models.DateField()

    def __str__(self):
        return f"caption:{self.caption}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="images")
    position = models.IntegerField(default=1)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name="tags")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
