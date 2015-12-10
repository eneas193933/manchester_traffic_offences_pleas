from django.core import mail
from django.test import TestCase, override_settings
from mock import patch

from ..forms import *
from ..messages import ERROR_MESSAGES

def reverse(url_name, *args, **kwargs):
    return "/path/to/" + url_name + "/"

class TestCourtAdminForms(TestCase):

    def setUp(self):
        valid_user = User()
        valid_user.username = "testuser"
        valid_user.email = "testuser@test.com"
        valid_user.first_name = "Frank"
        valid_user.last_name = "Marsh"
        valid_user.is_active = True
        valid_user.set_password("testpassword")
        valid_user.save()

        self.valid_user = valid_user

        inactive_user = User()
        inactive_user.username = "inactiveuser"
        valid_user.email = "inactiveuser@test.com"
        inactive_user.first_name = "John"
        inactive_user.last_name = "Doe"
        inactive_user.is_active = False
        inactive_user.set_password("testpassword")
        inactive_user.save()

        self.inactive_user = inactive_user

        self.court = Court.objects.create(court_code="0000",
                                          region_code="06",
                                          court_name="test court",
                                          court_address="test address",
                                          court_telephone="0800 MAKEAPLEA",
                                          court_email="test@test.com",
                                          submission_email="test@test.com",
                                          plp_email="test@test.com",
                                          enabled=True,
                                          test_mode=False)

    def test_login_form_no_data(self):

        form = CourtAdminAuthenticationForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 2)
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

    def test_login_form_invalid_login(self):

        form = CourtAdminAuthenticationForm(data={"username": "badusername",
                                                  "password": "badpassword"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn("INVALID_LOGIN", form.non_field_errors())

    def test_login_form_inactive_user(self):

        form = CourtAdminAuthenticationForm(data={"username": "inactiveuser",
                                                  "password": "testpassword"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn("INVALID_LOGIN", form.non_field_errors())

    def test_login_form_valid(self):

        form = CourtAdminAuthenticationForm(data={"username": "testuser",
                                                  "password": "testpassword"})

        valid = form.is_valid()

        self.assertTrue(valid)

    def test_password_reset_form_no_data(self):

        form = CourtAdminPasswordResetForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_REQUIRED"], form.errors["email"])

    def test_password_reset_form_invalid_email(self):

        form = CourtAdminPasswordResetForm(data={"email": "not an email"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_INVALID"], form.errors["email"])

    @override_settings(VALID_HMCTS_EMAIL_DOMAINS=["hmcts.gsi.gov.uk"])
    def test_password_reset_form_not_hmcts(self):

        form = CourtAdminPasswordResetForm(data={"email": "notvalid@example.com"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_HMCTS_INVALID"], form.errors["email"])

    def test_set_password_form_no_data(self):

        form = CourtAdminSetPasswordForm(self.valid_user,
                                         data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 2)
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_REQUIRED"], form.errors["new_password1"])
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_CONFIRM_REQUIRED"], form.errors["new_password2"])

    def test_set_password_form_password_mismatch(self):

        form = CourtAdminSetPasswordForm(self.valid_user,
                                         data={"new_password1": "password",
                                               "new_password2": "different"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["PASSWORD_MISMATCH"], form.errors["new_password2"])

    @patch("court_admin.forms.reverse", reverse)
    def test_send_username_reminder_email(self):

        context = {
            "host": "localhost",
            "use_https": True
        }
        UsernameReminderForm().send_username_reminder_email(self.valid_user, **context)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.valid_user.username, mail.outbox[-1].body)

    def test_username_reminder_form_no_data(self):

        form = UsernameReminderForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_REQUIRED"], form.errors["email"])

    def test_username_reminder_form_invalid_email(self):

        form = CourtAdminPasswordResetForm(data={"email": "not an email"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_INVALID"], form.errors["email"])

    @override_settings(VALID_HMCTS_EMAIL_DOMAINS=["hmcts.gsi.gov.uk"])
    def test_username_reminder_form_not_hmcts(self):

        form = CourtAdminPasswordResetForm(data={"email": "notvalid@example.com"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["EMAIL_HMCTS_INVALID"], form.errors["email"])

    def test_invite_get_random_username(self):

        random_username = InviteUserForm.get_random_username()

        self.assertRegexpMatches(random_username, r'^INVITE_.{23}')

    def test_invite_create_user(self):

        new_user = InviteUserForm().create_user("new_user@test.com",
                                                "Frank",
                                                "Marsh",
                                                self.court)

        self.assertIsInstance(new_user, User)
        self.assertEquals(new_user.email, "new_user@test.com")
        self.assertEquals(new_user.first_name, "Frank")
        self.assertEquals(new_user.last_name, "Marsh")

    def test_invite_create_user_from_form(self):

        form = InviteUserForm(data={"email": "new_user@test.com",
                                    "first_name": "Frank",
                                    "last_name": "Marsh",
                                    "court": self.court.id})

        form.is_valid()

        new_user = InviteUserForm().create_user_from_form(form)

        self.assertIsInstance(new_user, User)
        self.assertEquals(new_user.email, "new_user@test.com")
        self.assertEquals(new_user.first_name, "Frank")
        self.assertEquals(new_user.last_name, "Marsh")

    @patch("court_admin.forms.reverse", reverse)
    def test_invite_send_invite_email(self):

        context = {
            "host": "localhost",
            "use_https": True
        }
        InviteUserForm().send_invite_email(self.valid_user, **context)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.valid_user.first_name, mail.outbox[-1].body)

    def test_invite_user_form_no_data(self):

        form = InviteUserForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 4)
        self.assertIn(ERROR_MESSAGES["INVITE_EMAIL_REQUIRED"], form.errors["email"])
        self.assertIn(ERROR_MESSAGES["INVITE_FIRST_NAME_REQUIRED"], form.errors["first_name"])
        self.assertIn(ERROR_MESSAGES["INVITE_LAST_NAME_REQUIRED"], form.errors["last_name"])
        self.assertIn(ERROR_MESSAGES["COURT_REQUIRED"], form.errors["court"])

    def test_registration_verify_token(self):

        new_user = InviteUserForm().create_user("new_user@test.com",
                                                "Frank",
                                                "Marsh",
                                                self.court)

        token = token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))

        valid_token, user = RegistrationForm().verify_token(uid, token)

        self.assertTrue(valid_token)
        self.assertEqual(user, new_user)

    def test_registration_verify_token_invalid_token(self):

        user = User()
        user.first_name = "John"
        user.save()

        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes("4"))

        valid_token, test_user = RegistrationForm().verify_token(uid, token)

        self.assertFalse(valid_token)
        self.assertEquals(test_user, None)

    def test_registration_activate_user(self):

        form = RegistrationForm(data={"username": "frank.marsh",
                                      "first_name": "Frank",
                                      "last_name": "Marsh",
                                      "password1": "newpassword",
                                      "password2": "newpassword"})

        form.is_valid()

        form.activate_user(self.inactive_user)

        self.assertTrue(self.inactive_user.is_active)

    def test_registration_form_no_data(self):

        form = RegistrationForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 5)
        self.assertIn(ERROR_MESSAGES["NEW_USERNAME_REQUIRED"], form.errors["username"])
        self.assertIn(ERROR_MESSAGES["FIRST_NAME_REQUIRED"], form.errors["first_name"])
        self.assertIn(ERROR_MESSAGES["LAST_NAME_REQUIRED"], form.errors["last_name"])
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_REQUIRED"], form.errors["password1"])
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_CONFIRM_REQUIRED"], form.errors["password2"])

    def test_registration_form_username_taken(self):

        form = RegistrationForm(data={"username": "testuser",
                                      "first_name": "Frank",
                                      "last_name": "Marsh",
                                      "password1": "newpassword",
                                      "password2": "newpassword"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["NEW_USERNAME_TAKEN"], form.errors["username"])

    def test_personal_details_form_no_data(self):

        form = PersonalDetailsForm(data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 4)
        self.assertIn(ERROR_MESSAGES["NEW_USERNAME_REQUIRED"], form.errors["username"])
        self.assertIn(ERROR_MESSAGES["FIRST_NAME_REQUIRED"], form.errors["first_name"])
        self.assertIn(ERROR_MESSAGES["LAST_NAME_REQUIRED"], form.errors["last_name"])
        self.assertIn(ERROR_MESSAGES["EMAIL_REQUIRED"], form.errors["email"])

    def test_password_change_form_no_data(self):

        form = CourtAdminPasswordChangeForm(self.valid_user,
                                            data={})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 3)
        self.assertIn(ERROR_MESSAGES["OLD_PASSWORD_REQUIRED"], form.errors["old_password"])
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_REQUIRED"], form.errors["new_password1"])
        self.assertIn(ERROR_MESSAGES["NEW_PASSWORD_CONFIRM_REQUIRED"], form.errors["new_password2"])

    def test_password_change_form_incorrect_password(self):

        form = CourtAdminPasswordChangeForm(self.valid_user,
                                            data={"old_password": "wrong password",
                                                  "new_password1": "new password",
                                                  "new_password2": "new password"})

        form.is_valid()

        self.assertEquals(len(form.errors.items()), 1)
        self.assertIn(ERROR_MESSAGES["OLD_PASSWORD_INCORRECT"], form.errors["old_password"])
