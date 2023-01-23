from django.urls import reverse
from djangogramm.models import Like
from djangogramm.tests import (PostBaseTestCase, create_test_like,
                               create_test_post, create_test_profile)


class CreateLikeTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'like-create'

    def test_post(self):
        response = self.client.post(reverse(self.viewname, kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.filter(profile=self.profile, post=self.post).count(), 1)

    def test_post_post_not_exists(self):
        self.post.delete()

        response = self.client.post(reverse(self.viewname, kwargs={'post_id': 99}))
        self.assertEqual(response.status_code, 404)

        self.post = create_test_post(self.profile)

    def test_post_profile_not_exists(self):
        self.profile.delete()

        response = self.client.post(reverse(self.viewname, kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)


class DeleteLikeTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'like-delete'

    def test_post(self):
        create_test_like(profile=self.profile, post=self.post)
        response = self.client.post(reverse(self.viewname, kwargs={'post_id': self.post.id}))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(post=self.post)

    def test_post_like_does_not_exists(self):
        response = self.client.post(reverse(self.viewname, kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 404)

    def test_post_post_not_exists(self):
        self.post.delete()

        response = self.client.post(reverse(self.viewname, kwargs={'post_id': 99}))
        self.assertEqual(response.status_code, 404)

        self.post = create_test_post(self.profile)

    def test_post_profile_not_exists(self):
        self.profile.delete()

        response = self.client.post(reverse(self.viewname, kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 404)

        self.profile = create_test_profile(self.user)