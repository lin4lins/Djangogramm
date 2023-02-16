from datetime import datetime
from random import choice, randint, sample, shuffle

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import requests
from PIL import Image as PIL_Image

from djangogramm.models import Profile, Post, Image, Like, Follower
from signup.models import User

PROFILES_COUNT = 10
MIN_POSTS_PER_PROFILE = 0
MAX_POSTS_PER_PROFILE = 10
MAX_CHARS_FOR_CAPTION = 255

MAX_CHARS_FOR_BIO = 255
MIN_TAGS_PER_POST = 0
MAX_TAGS_PER_POST = 3

MIN_IMAGES_PER_POST = 1
MAX_IMAGES_PER_POST = 4

IMG_SIZES_IN_PX = list(range(300, 1001, 100))

faker = Faker('en_US')


class Command(BaseCommand):
    help = 'Populates database with fake profiles, posts, images, likes and tags'

    def add_arguments(self, parser):
        parser.add_argument('--profiles', '-pr', type=int, help='Must be equal to users count')
        parser.add_argument('--posts', '-po', type=int, help='Max posts per profile')
        parser.add_argument('--images', '-i', type=int, help='Max images per post')


    def handle(self, *args, **options):
        if options['profiles']:
            if options['profiles'] > User.objects.all().count():
                raise CommandError('Profiles count can not be greater than users count')

        self.__create_fake_profiles(options['profiles']) if  options['profiles'] else self.__create_fake_profiles()
        self.__create_fake_posts(options['posts']) if  options['posts'] else self.__create_fake_posts()
        self.__create_fake_images(options['images']) if options['images'] else self.__create_fake_images()
        self.__create_fake_likes()
        self.__create_fake_followers()

    def __create_fake_profiles(self, profiles_count=PROFILES_COUNT):
        for user_id in range(1, profiles_count+1):
            profile_data = faker.simple_profile()
            bio = faker.text(max_nb_chars=MAX_CHARS_FOR_BIO)
            user = User.objects.get(id=user_id)
            avatar_path = f'avatars/{user_id}-avatar.jpg'
            Command.__download_image(avatar_path)
            Profile.objects.create(user=user, full_name=profile_data['name'], bio=bio, avatar=avatar_path)

        self.stdout.write("Profiles created successfully")

    def __create_fake_posts(self, max_posts=MAX_POSTS_PER_PROFILE):
        for profile in Profile.objects.all():
            for _ in range(randint(MIN_POSTS_PER_PROFILE, max_posts)):
                caption_without_hashtags = faker.text(max_nb_chars=MAX_CHARS_FOR_CAPTION)
                caption_with_hashtags = self.__add_tags_to_caption(caption_without_hashtags)
                post = Post(author=profile, caption=caption_with_hashtags)
                post.save()
                post.created_at = faker.date_time_between_dates(datetime(2020,1,1,0,0,0), datetime.now())
                post.save()

        self.stdout.write("Posts created successfully")

    def __create_fake_images(self, max_images=MAX_IMAGES_PER_POST):
        for post in Post.objects.all():
            for position in range(randint(MIN_IMAGES_PER_POST, max_images)):
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

    def __create_fake_followers(self):
        followers = list(Profile.objects.all())
        following = followers.copy()
        shuffle(followers)
        shuffle(following)
        for follower_profile in followers:
            for following_profile in following:
                if len(Follower.objects.filter(who_follows=follower_profile, who_is_followed=following_profile)) != 0:
                    continue
                if faker.boolean():
                    Follower.objects.create(who_follows=follower_profile, who_is_followed=following_profile)

        self.stdout.write("Followers created successfully")

    @staticmethod
    def __download_image(image_path: str):
        image_size_px = choice(IMG_SIZES_IN_PX)
        response = requests.get(f'https://picsum.photos/{image_size_px}/{image_size_px}', stream=True)
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