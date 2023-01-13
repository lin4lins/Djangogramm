from datetime import datetime
from random import choice, randint, sample

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import requests
from PIL import Image as PIL_Image

from djangogramm.models import Profile, Post, Image, Like
from signup.models import User

PROFILES_COUNT = 2
MIN_POSTS_PER_PROFILE = 0
MAX_POSTS_PER_PROFILE = 10
MAX_CHARS_FOR_CAPTION = 255

MAX_CHARS_FOR_BIO = 255
MIN_TAGS_PER_POST = 0
MAX_TAGS_PER_POST = 3

MIN_IMAGES_PER_POST = 1
MAX_IMAGES_PER_POST = 4

IMG_SIZES_IN_PX = list(range(300, 1301, 100))

faker = Faker('en_US')


class Command(BaseCommand):
    help = 'Populates database with fake profiles, posts, images, likes and tags'

    def handle(self, *args, **options):
        self.__create_fake_profiles()
        self.__create_fake_posts()
        self.__create_fake_images()
        self.__create_fake_likes()

    def __create_fake_profiles(self):
        for user_id in range(1, PROFILES_COUNT+1):
            profile_data = faker.simple_profile()
            bio = faker.text(max_nb_chars=MAX_CHARS_FOR_BIO)
            user = User.objects.get(id=user_id)
            avatar_path = f'avatars/{user_id}-avatar.jpg'
            Command.__download_image(avatar_path)
            Profile.objects.create(user=user, full_name=profile_data['name'], bio=bio, avatar=avatar_path)

        self.stdout.write("Profiles created successfully")

    def __create_fake_posts(self):
        for profile in Profile.objects.all():
            for _ in range(randint(MIN_POSTS_PER_PROFILE, MAX_POSTS_PER_PROFILE)):
                caption_without_hashtags = faker.text(max_nb_chars=MAX_CHARS_FOR_CAPTION)
                caption_with_hashtags = self.__add_tags_to_caption(caption_without_hashtags)
                post = Post(author=profile, caption=caption_with_hashtags)
                post.save()
                post.created_at = faker.date_time_between_dates(datetime(2020,1,1,0,0,0), datetime.now())
                post.save()

        self.stdout.write("Posts created successfully")

    def __create_fake_images(self):
        for post in Post.objects.all():
            for position in range(randint(MIN_IMAGES_PER_POST, MAX_IMAGES_PER_POST)):
                original_image_path = f'posts/originals/{post.id}-{position}.jpg'
                original_image = self.__download_image(original_image_path)

                preview_image = original_image.copy()
                preview_image_path = f'posts/previews/{post.id}-{position}.jpg'
                preview_image.save(f'media/{preview_image_path}')

                Image(post=post, original=original_image_path, preview=preview_image_path, position=position).save()

        self.stdout.write("Images created successfully")

    def __create_fake_likes(self):
        for post in Post.objects.all():
            for profile in Profile.objects.all():
                if faker.boolean():
                    Like.objects.create(post=post, profile=profile)

        self.stdout.write("Likes created successfully")

    @staticmethod
    def __download_image(image_path: str):
        image_width_px, image_height_px = choice(IMG_SIZES_IN_PX), choice(IMG_SIZES_IN_PX)
        response = requests.get(f'https://picsum.photos/{image_width_px}/{image_height_px}', stream=True)
        if response.status_code != 200:
            raise CommandError("While profile image downloading an error occurred")

        response.raw.decode_content = True
        with PIL_Image.open(response.raw) as img:
            img.save(f'media/{image_path}')
            response.close()
            return img

    @staticmethod
    def __add_tags_to_caption(caption: str):
        words = caption.split()
        hashtag_words = sample(words, randint(MIN_TAGS_PER_POST, MAX_TAGS_PER_POST))
        for word_index, word in enumerate(words):
            for hashtag_word in hashtag_words:
                if word == hashtag_word:
                    words[word_index] = f'#{hashtag_word.strip(".")}'.lower()

        return ' '.join(words)