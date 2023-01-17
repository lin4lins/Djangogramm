from django.urls import reverse
from djangogramm.models import Profile
from djangogramm.tests import (BaseTestCase, create_test_profile,
                               create_test_user, get_profile_form_data, ProfileBaseTestCase)


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

        profile.delete()
        user.delete()

    def test_get_profile_not_exists(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'test99'}))

        self.assertEqual(response.status_code, 404)


class ProfileMeTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('profile-me')

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile-me.html')

    def test_get_profile_not_exists(self):
        self.profile.delete()

        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)


class ProfileUpdateTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('profile-update')

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/profile_update.html')

    def test_get_profile_not_exists(self):
        self.profile.delete()
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)

    def test_post(self):
        response = self.client.post(self.path, data=get_profile_form_data())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-me'))

    def test_post_profile_not_exists(self):
        self.profile.delete()

        response = self.client.post(self.path, data=get_profile_form_data())
        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)

    def test_post_invalid_form(self):
        data = get_profile_form_data('pdf.pdf')
        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')