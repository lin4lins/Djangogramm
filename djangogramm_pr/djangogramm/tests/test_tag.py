from django.urls import reverse

from djangogramm.models import Tag
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


    def test_get_profile_not_exists(self):
        tag = create_test_tag(self.post)
        self.profile.delete()

        response = self.client.get(reverse(self.viewname, kwargs={'name': tag.name}))
        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)