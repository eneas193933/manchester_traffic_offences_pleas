from django.contrib.auth.tokens import PasswordResetTokenGenerator


# probably best to subclass and change the hmac salt
token_generator = PasswordResetTokenGenerator()
