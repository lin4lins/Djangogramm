import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


confirmation_token = ConfirmationTokenGenerator()
