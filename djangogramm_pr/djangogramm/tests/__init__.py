from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TransactionTestCase, override_settings
from djangogramm.models import Profile, Post, Image
from signup.models import User

VALID_USER_FORM_DATA = {'email': 'test2@gmail.com',
                        'username': 'test2',
                        'password': 'HelloWorld2'}

def create_test_user(email=VALID_USER_FORM_DATA['email'], username=VALID_USER_FORM_DATA['username']) -> User:
    user = User(email=email, username=username, is_active=True)
    user.set_password(VALID_USER_FORM_DATA['password'])
    user.save()
    return user

def get_profile_form_data(filename: str = 'profile_pic.jpeg') -> dict:
    filename, filetype = filename.split('.')
    path_to_image = Path(__file__).parent / 'test_media' / f'{filename}.{filetype}'
    profile_form_data = {'full_name': 'Test Tester',
                               'bio': 'Test Bio'}
    with open(path_to_image, 'rb') as file:
        content = file.read()
        profile_form_data['avatar'] = SimpleUploadedFile(name=f'{filename}.{filetype}', content=content)
        return profile_form_data

def create_test_profile(user: User) -> Profile:
    data = get_profile_form_data()
    return Profile.objects.create(user=user, full_name=data['full_name'], bio=data['bio'], avatar=data['avatar'])

def get_post_form_data(filename: str = 'post.jpg') -> dict:
    filename, filetype = filename.split('.')
    media = []
    for i in range(1, 4):
        path_to_image = Path(__file__).parent / 'test_media' / f'{filename}{i}.{filetype}'
        with open(path_to_image, 'rb') as file:
            content = file.read()
            media.append(SimpleUploadedFile(name=f'{filename}{i}.{filetype}', content=content))

    return {'caption': 'Test Caption For #post', 'original': media}

def create_test_post(profile: Profile) -> Post:
    data = get_post_form_data()
    post = Post(author=profile, caption=data['caption']).save()
    for position, image in enumerate(data['original']):
        Image(post=post, original=image, preview=image, position=position).save()

    return post

@override_settings(MEDIA_ROOT=Path(__file__).parent / 'test_storage')
class BaseTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.user.delete()


class ProfileBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.profile = create_test_profile(self.user)

    def tearDown(self):
        super().tearDown()
        self.profile.delete()


class PostBaseTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.post = create_test_post(self.profile)

    def tearDown(self):
        super().tearDown()
        self.post.delete()