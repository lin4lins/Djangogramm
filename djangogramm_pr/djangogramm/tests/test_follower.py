from django.urls import reverse

from djangogramm.models import Follower
from djangogramm.tests import ProfileBaseTestCase, create_test_profile, create_test_user, create_test_follower


class CreateFollowTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'follow-create'

    def test_post(self):
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_follow = create_test_profile(user_to_follow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow.username}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follower.objects.filter(who_follows=self.profile, who_is_followed=profile_to_follow).count(), 1)

        Follower.objects.get(who_follows=self.profile, who_is_followed=profile_to_follow).delete()
        profile_to_follow.delete()
        user_to_follow.delete()

    def test_post_user_to_follow_not_exists(self):
        response = self.client.post(reverse(self.viewname, kwargs={'username': 'test99'}))
        self.assertEqual(response.status_code, 404)


    def test_post_profile_to_follow_not_exists(self):
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow}))
        self.assertEqual(response.status_code, 404)

        user_to_follow.delete()

    def test_post_following_profile_not_exists(self):
        self.profile.delete()
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_follow = create_test_profile(user_to_follow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow.username}))
        self.assertEqual(response.status_code, 404)

        profile_to_follow.delete()
        user_to_follow.delete()
        self.profile = create_test_profile(self.user)


    def test_follower_already_exists(self):
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_follow = create_test_profile(user_to_follow)
        follower = Follower.objects.create(who_follows=self.profile, who_is_followed=profile_to_follow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow.username}))
        self.assertEqual(response.status_code, 404)

        follower.delete()
        profile_to_follow.delete()
        user_to_follow.delete()


class DeleteFollowTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'follow-delete'

    def test_post(self):
        user_to_unfollow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_unfollow = create_test_profile(user_to_unfollow)
        follower = create_test_follower(who_follows=self.profile, who_is_followed=profile_to_unfollow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_unfollow.username}))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Follower.DoesNotExist):
            Follower.objects.get(who_follows=self.profile, who_is_followed=profile_to_unfollow)

        profile_to_unfollow.delete()
        user_to_unfollow.delete()

    def test_post_user_to_unfollow_not_exists(self):
        response = self.client.post(reverse(self.viewname, kwargs={'username': 'test99'}))
        self.assertEqual(response.status_code, 404)

    def test_post_profile_to_unfollow_not_exists(self):
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow}))
        self.assertEqual(response.status_code, 404)

        user_to_follow.delete()

    def test_post_following_profile_not_exists(self):
        self.profile.delete()
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_follow = create_test_profile(user_to_follow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow.username}))
        self.assertEqual(response.status_code, 404)

        profile_to_follow.delete()
        user_to_follow.delete()
        self.profile = create_test_profile(self.user)

    def test_follower_not_exists(self):
        user_to_follow = create_test_user(email='test99@gmail.com', username='test99')
        profile_to_follow = create_test_profile(user_to_follow)

        response = self.client.post(reverse(self.viewname, kwargs={'username': user_to_follow.username}))
        self.assertEqual(response.status_code, 404)

        profile_to_follow.delete()
        user_to_follow.delete()