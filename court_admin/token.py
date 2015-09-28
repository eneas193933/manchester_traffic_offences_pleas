from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36
import six


class UserInvitePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):
        """
        Method copied verbatim from the parent class so that the key_salt var
        can be modified.
        """

        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # By hashing on the internal state of the user and using state
        # that is sure to change (the password salt will change as soon as
        # the password is set, at least for current Django auth, and
        # last_login will also change), we produce a hash that will be
        # invalid as soon as it is used.
        # We limit the hash to 20 chars to keep URL short
        key_salt = "manchester_traffic_offences_pleas.court_admin.tokens.PasswordResetTokenGenerator"

        # Ensure results are consistent across DB backends
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)

        value = (six.text_type(user.pk) + user.password +
                six.text_type(login_timestamp) + six.text_type(timestamp))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)


token_generator = UserInvitePasswordResetTokenGenerator()
