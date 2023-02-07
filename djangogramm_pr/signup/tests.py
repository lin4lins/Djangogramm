from django.conf import settings
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from signup.models import User
from signup.utils import confirmation_token

# Create your tests here.

VALID_USER_FORM_DATA = {'email': 'test1@gmail.com',
                        'username': 'test1',
                        'password1': 'HelloWorld1',
                        'password2': 'HelloWorld1'}


def create_test_user() -> User:
    user = User(email=VALID_USER_FORM_DATA['email'], username=VALID_USER_FORM_DATA['username'], is_active=False)
    user.set_password(VALID_USER_FORM_DATA['password1'])
    user.save()
    return user


class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.viewname = 'signup'
        self.path = reverse(self.viewname)
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    def test_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup.html')

    def test_post(self):
        response = self.client.post(self.path, data=VALID_USER_FORM_DATA)
        user = User.objects.get(username=VALID_USER_FORM_DATA['username'])

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check your email')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Confirm your email to sign in Djangogramm!')

        user.delete()

    def test_post_username_already_exists(self):
        user = create_test_user()
        response = self.client.post(self.path, data=VALID_USER_FORM_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup.html')
        self.assertContains(response, 'A user with that username already exists.')
        self.assertContains(response, 'User with this Email already exists.')

        user.delete()


class ConfirmationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.viewname = 'confirm'

    def tearDown(self):
        self.user.delete()

    def test_get(self):
        response = self.client.get(self.__get_confirmation_link())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/confirmed.html')

    def test_invalid_uidb64(self):
        response = self.client.get(self.__get_confirmation_link(is_uidb64_invalid=True))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'Invalid confirmation link')

    def test_user_does_not_exist(self):
        response = self.client.get(self.__get_confirmation_link(is_user_exist=False))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'Invalid confirmation link')

    def test_user_is_active(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.get(self.__get_confirmation_link())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/confirmed_earlier.html')
        self.assertContains(response, 'You have already confirmed your email')
        
    def __get_confirmation_link(self, is_uidb64_invalid=False, is_token_invalid=False, is_user_exist=True) -> str:
        user_id = self.user.id if is_user_exist else 99
        uidb64 = 'a12*' if is_uidb64_invalid else urlsafe_base64_encode(force_bytes(user_id))
        token = 'helloworld' if is_token_invalid else confirmation_token.make_token(self.user)
        return reverse(self.viewname, kwargs={'uidb64': uidb64, 'token': token})
