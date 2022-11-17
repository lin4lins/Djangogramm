from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    confirmation_link = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=255, null=True)
    avatar_path = models.ImageField(upload_to="avatars", null=True)

    def __str__(self):
        return f"id: {self.id} full_name:{self.full_name}"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    publication_date = models.DateField()

    def __str__(self):
        return f"id: {self.id} caption:{self.caption}"


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="images")
    position = models.IntegerField(default=1)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name="tags")


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
