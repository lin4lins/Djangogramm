from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TransactionTestCase
from djangogramm.models import Profile
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
    path_to_file = Path(__file__).parent / 'test_media' / filename
    valid_profile_form_data = {'full_name': 'Test Tester',
                               'bio': 'Test Bio'}
    with open(path_to_file, 'rb') as file:
        content = file.read()
        valid_profile_form_data['avatar'] = SimpleUploadedFile(name='profile_pic.jpeg',
                                    content=content,
                                    content_type='image/jpeg')
        return valid_profile_form_data

def create_test_profile(user: User) -> User:
    data = get_profile_form_data()
    return Profile.objects.create(user=user, full_name=data['full_name'], bio=data['bio'], avatar=data['avatar'])


class BaseTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.user.delete()
