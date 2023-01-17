from django.test import Client, TransactionTestCase

from signup.models import User

VALID_USER_FORM_DATA = {'email': 'test2@gmail.com',
                        'username': 'test2',
                        'password': 'HelloWorld2'}

def create_test_user(email=VALID_USER_FORM_DATA['email'], username=VALID_USER_FORM_DATA['username']) -> User:
    user = User(email=email, username=username, is_active=True)
    user.set_password(VALID_USER_FORM_DATA['password'])
    user.save()
    return user


class BaseTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.user.delete()
