from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGES = {
    "USERNAME_REQUIRED": _("Enter your username"),
    "PASSWORD_REQUIRED": _("Enter your password"),
    "EMAIL_REQUIRED": _("Enter your email address"),
    "EMAIL_INVALID": _("Email address isn't a valid format"),
    "EMAIL_HMCTS_INVALID": _("Email must be a valid HMCTS address"),
    "OLD_PASSWORD_REQUIRED": _("Enter your current password"),
    "OLD_PASSWORD_INCORRECT": _("The password you entered is incorrect"),
    "NEW_PASSWORD_REQUIRED": _("Enter your new password"),
    "NEW_PASSWORD_CONFIRM_REQUIRED": _("Enter your new password again"),
    "PASSWORD_MISMATCH": _("Passwords do not match, check and try again"),
    "PASSWORD_MIN_LENGTH": _("Create a password using at least 6 characters"),
    "NEW_USERNAME_REQUIRED": _("Enter your desired username"),
    "NEW_USERNAME_TAKEN": _("This username is already taken"),
    "FIRST_NAME_REQUIRED": _("Enter your first name"),
    "LAST_NAME_REQUIRED": _("Enter your last name"),
    "INVITE_EMAIL_REQUIRED": _("Enter the user's email address"),
    "INVITE_FIRST_NAME_REQUIRED": _("Enter the user's first name"),
    "INVITE_LAST_NAME_REQUIRED": _("Enter the user's last name"),
    "COURT_REQUIRED": _("Select the court this user can access"),
}
