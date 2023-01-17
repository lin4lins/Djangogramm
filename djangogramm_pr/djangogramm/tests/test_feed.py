from django.urls import reverse
from djangogramm.tests import BaseTestCase
from djangogramm.tests.test_profile import create_test_profile


class FeedTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = reverse('feed')

    def test_get(self):
        profile = create_test_profile(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/feed.html')

        profile.delete()

    def test_get_not_existing_profile(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 404)
