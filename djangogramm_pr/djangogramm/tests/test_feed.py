from django.urls import reverse
from djangogramm.tests import ProfileBaseTestCase, create_test_profile


class FeedTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'feed'
        self.path = reverse(self.viewname)

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/feed.html')

    def test_get_no_profile(self):
        self.profile.delete()
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-create'))

        self.profile = create_test_profile(self.user)