from django.urls import reverse
from faker import Faker

from djangogramm.models import (Post, Image, Tag)
from djangogramm.tests import (ProfileBaseTestCase, create_test_post,
                               create_test_profile, create_test_user,
                               get_post_form_data)


class PostCreateTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'post-create'
        self.path = reverse(self.viewname)

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djangogramm/post_create.html')

    def test_get_no_profile(self):
        self.profile.delete()
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-create'))

        self.profile = create_test_profile(self.user)

    def test_post(self):
        response = self.client.post(self.path, data=get_post_form_data())
        post = Post.objects.get(author=self.profile)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('feed'))
        self.assertEqual(post.media.all().count(), 3)
        self.assertEqual(post.tags.all().count(), 1)

        post.delete()

    def test_post_invalid_files(self):
        data = get_post_form_data('pdf_post.pdf')
        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('post-create'))

    def test_post_invalid_caption(self):
        data = get_post_form_data()
        faker = Faker('en_US')
        data['caption'] = faker.text(max_nb_chars=2000)
        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('post-create'))


class PostDeleteTestCase(ProfileBaseTestCase):
    def setUp(self):
        super().setUp()
        self.viewname = 'post-delete'

    def test_get(self):
        post = create_test_post(self.profile)
        response = self.client.get(reverse(self.viewname, kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile-me'))
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)

        self.assertEqual(Image.objects.filter(post=post).count(), 0)
        self.assertEqual(Tag.objects.filter(posts=post).count(), 0)

    def test_get_wrong_post_author(self):
        user = create_test_user(email='test99@gmail.com', username='test99')
        profile = create_test_profile(user)
        post = create_test_post(profile)

        response = self.client.get(reverse(self.viewname, kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 404)

        post.delete()
        profile.delete()
        user.delete()

    def test_get_post_not_exists(self):
        response = self.client.get(reverse(self.viewname, kwargs={'id': 99}))
        self.assertEqual(response.status_code, 404)
