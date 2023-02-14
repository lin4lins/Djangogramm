import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image as PIL_Image
from django.shortcuts import get_object_or_404

from signup.models import User

from djangogramm.managers import PostQuerySet
from mysite.storage_backends import PublicMediaStorage


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    full_name = models.CharField(max_length=100, null=False)
    bio = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to="avatars/", storage=PublicMediaStorage(), null=True, blank=True)

    def __str__(self):
        return f'full_name:{self.full_name}, bio:{self.bio}'


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'posts')
    caption = models.CharField(null=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostQuerySet().as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__add_tags()
        return self

    def __add_tags(self):
        for tag in self.get_tags_from_caption():
            if len(Tag.objects.filter(name=tag)) == 0:
                tag_to_add = Tag.objects.create(name=tag)
            else:
                tag_to_add = get_object_or_404(Tag, name=tag)

            self.tags.add(tag_to_add)

    def get_tags_from_caption(self) -> list:
        return [word.replace('#', '') for word in self.caption.split() if word[0] == '#']

    def __str__(self):
        return f'caption:{self.caption}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'media')
    original = models.ImageField(upload_to='posts/originals/', storage=PublicMediaStorage())
    preview = models.ImageField(upload_to='posts/previews/', storage=PublicMediaStorage())
    position = models.IntegerField(default=0)

    def save_with_compress(self, *args, **kwargs):
        self.__create_preview()
        super().save(*args, **kwargs)

    def __create_preview(self):
        output_thumb = BytesIO()
        img = PIL_Image.open(self.original)
        image_format = self.original.file.name.rsplit('.', 1)[1]
        image_format = 'jpeg' if image_format == 'jpg' else image_format
        img.save(output_thumb, format=image_format, quality=60)
        self.preview = InMemoryUploadedFile(file=output_thumb, field_name='ImageField', name=self.original.file.name,
                                            content_type=self.original.file.content_type,
                                            size=sys.getsizeof(output_thumb), charset=None)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    posts = models.ManyToManyField(Post, related_name='tags')


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'likes')


class Follower(models.Model):
    who_follows = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'following')
    who_is_followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
