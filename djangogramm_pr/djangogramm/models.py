from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from signup.models import User


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    bio = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True)

    def __str__(self):
        return f"full_name:{self.full_name}, bio:{self.bio}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(null=True, max_length=255)
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"caption:{self.caption}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="posts/")
    position = models.IntegerField(default=1)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name="tags")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
