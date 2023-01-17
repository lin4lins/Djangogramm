from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from pathlib import Path
from djangogramm.models import Profile
from djangogramm.tests import BaseTestCase, create_test_user
from signup.models import User


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


class ProfileCreateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('profile-create')

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile_create.html')

    def test_get_profile_already_exists(self):
        profile = create_test_profile(self.user)

        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

        profile.delete()

    def test_post(self):
        response = self.client.post(self.path, data=get_profile_form_data())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-me'))

        Profile.objects.get(user=self.user).delete()

    def test_post_profile_already_exists(self):
        profile = create_test_profile(self.user)
        response = self.client.post(self.path, data=get_profile_form_data())

        self.assertEqual(response.status_code, 404)

        profile.delete()

    def test_post_invalid_form(self):
        data = get_profile_form_data('pdf.pdf')
        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')


class ProfileTestCase(BaseTestCase):
    def test_get_me(self):
        profile = create_test_profile(self.user)
        response = self.client.get(reverse('profile', kwargs={'username': profile.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile.html')

        profile.delete()

    def test_get_profile(self):
        user = create_test_user(email='test99@gmail.com', username='test99')
        profile = create_test_profile(user)
        response = self.client.get(reverse('profile', kwargs={'username': profile.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile.html')

        user.delete()
        profile.delete()

    def test_get_not_existing_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'test99'}))

        self.assertEqual(response.status_code, 404)


class ProfileMeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('profile-me')

    def test_get(self):
        profile = create_test_profile(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile-me.html')

        profile.delete()

    def test_get_not_existing_profile(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 404)


class ProfileUpdateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('profile-update')

    def test_get(self):
        profile = create_test_profile(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile_update.html')

        profile.delete()

    def test_get_not_existing_profile(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 404)

    def test_post(self):
        profile = create_test_profile(self.user)
        response = self.client.post(self.path, data=get_profile_form_data())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-me'))

        profile.delete()

    def test_post_not_existing_profile(self):
        response = self.client.post(self.path, data=get_profile_form_data())

        self.assertEqual(response.status_code, 404)

    def test_post_invalid_form(self):
        profile = create_test_profile(self.user)
        data = get_profile_form_data('pdf.pdf')
        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

        profile.delete()