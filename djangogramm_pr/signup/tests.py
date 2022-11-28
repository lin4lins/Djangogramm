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
                        'password1': 'HelloWorld1',
                        'password2': 'HelloWorld1'}


def create_test_user() -> User:
    user = User(email=VALID_USER_FORM_DATA['email'])
    user.set_password(VALID_USER_FORM_DATA['password1'])
    user.save()
    return user


class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()
        self.path = reverse('signup')
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_post(self):
        response = self.client.post(self.path, data=VALID_USER_FORM_DATA)
        User.users.get(email=VALID_USER_FORM_DATA['email'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check your email')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Confirm your email to sign in Djangogramm!')

    def test_post_email_already_exists(self):
        create_test_user()
        response = self.client.post(self.path, data=VALID_USER_FORM_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors.html')
        self.assertContains(response, 'User with this Email already exists')


class TestConfirmationView(TestCase):
    valid_user_data = {'email': 'test1@gmail.com',
                       'password1': 'HelloWorld1',
                       'password2': 'HelloWorld1'}

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(self.__get_confirmation_link())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_uidb64(self):
        response = self.client.get(self.__get_confirmation_link(is_uidb64_invalid=True))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid confirmation link')


    def test_user_does_not_exist(self):
        response = self.client.get(self.__get_confirmation_link(is_user_exist=False))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid confirmation link')

    def test_confirmation_link_used_twice(self):
        confirmation_link = self.__get_confirmation_link()
        self.client.get(confirmation_link)
        response = self.client.get(confirmation_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have already confirmed your email')
        
    @staticmethod
    def __get_confirmation_link(is_uidb64_invalid=False, is_token_invalid=False, is_user_exist=True) -> str:
        user = create_test_user()
        user_id = user.pk if is_user_exist else 99
        uidb64 = 'a1' if is_uidb64_invalid else urlsafe_base64_encode(force_bytes(user_id))
        token = 'helloworld' if is_token_invalid else confirmation_token.make_token(user)
        return reverse('confirm', kwargs={'uidb64': uidb64, 'token': token})
