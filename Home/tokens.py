from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from .models import Profile


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(Profile.profile_id) + six.text_type(timestamp) + six.text_type(Profile.is_active)
        )


account_activation_token = TokenGenerator()