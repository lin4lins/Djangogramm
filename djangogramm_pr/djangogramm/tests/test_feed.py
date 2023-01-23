from django.urls import reverse
from djangogramm.tests import ProfileBaseTestCase
from djangogramm.tests.test_profile import create_test_profile


class FeedTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'feed'
        self.path = reverse(self.viewname)

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/feed.html')