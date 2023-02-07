from django.urls import reverse

from djangogramm.tests import create_test_profile, create_test_tag, PostBaseTestCase


class TagTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'tag'

    def test_get(self):
        tag = create_test_tag(self.post)
        response = self.client.get(reverse(self.viewname, kwargs={'name': tag.name}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/tag.html')

        tag.delete()

    def test_get_tag_not_exists(self):
        response = self.client.get(reverse(self.viewname, kwargs={'name': 'abc'}))
        self.assertEqual(response.status_code, 404)

    def test_get_no_profile(self):
        self.profile.delete()
        response = self.client.get(reverse(self.viewname, kwargs={'name': 'abc'}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-create'))

        self.profile = create_test_profile(self.user)
