from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView, RedirectView
from court_admin.forms import (CourtAdminAuthenticationForm,
                               CourtAdminPasswordResetForm,
                               CourtAdminPasswordChangeForm)
from views import (DashboardView,
                   UsersView,
                   InviteUserView,
                   RegisterView,
                   UsernameReminderView,
                   PersonalDetailsView)


urlpatterns = patterns("",
    url(r"^$", RedirectView.as_view(pattern_name="dashboard", permanent=True)),

    url(r"^dashboard/$", DashboardView.as_view(),
        name="dashboard"),
    url(r"^dashboard/(?P<year>\d+)/(?P<month>\d+)$", DashboardView.as_view(),
        name="dashboard"),
    url(r"^dashboard/(?P<court_id>\d+)/$", DashboardView.as_view(),
        name="dashboard"),
    url(r"^dashboard/(?P<court_id>\d+)/(?P<year>\d+)/(?P<month>\d+)$", DashboardView.as_view(),
        name="dashboard"),

    url(r"^users/$", UsersView.as_view(), name="users"),
    url(r"^users/invite/$", InviteUserView.as_view(), name="invite_user"),

    url(r"^register/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", RegisterView.as_view(), name="register"),
    url(r"^register/done/$", TemplateView.as_view(template_name="profile/register_done.html"), name="register_done"),

    url(r"^sign-in/$", auth_views.login,
        {"template_name": "profile/login.html",
         "authentication_form": CourtAdminAuthenticationForm},
        name="login"),
    url(r"^sign-out/$", auth_views.logout_then_login,
        {"login_url": "/sign-in/"},
        name="logout"),

    url(r"^forgotten-password/$", auth_views.password_reset,
        {"template_name": "profile/password_reset_form.html",
         "password_reset_form": CourtAdminPasswordResetForm,
         "email_template_name": "emails/password_reset.txt",
         "subject_template_name": "emails/password_reset_subject.txt"},
        name="password_reset"),
    url(r"^forgotten-password/done/$", auth_views.password_reset_done,
        {"template_name": "profile/password_reset_done.html"},
        name="password_reset_done"),

    url(r"^forgotten-username/$", UsernameReminderView.as_view(),
        name="forgotten_username"),
    url(r"^forgotten-username/done/$", TemplateView.as_view(template_name="profile/forgotten_username_done.html"),
        name="forgotten_username_done"),

    url(r"^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm,
        {"template_name": "profile/password_reset_confirm.html"},
        name="password_reset_confirm"),
    url(r"^reset-password/done/$", auth_views.password_reset_complete,
        {"template_name": "profile/password_reset_complete.html"},
        name="password_reset_complete"),

    url(r"^settings/personal-details/$", PersonalDetailsView.as_view(), name="personal_details"),
    url(r"^settings/personal-details/done/$", TemplateView.as_view(template_name="settings/personal_details_done.html"), name="personal_details_done"),
    url(r"^settings/change-password/$", auth_views.password_change,
        {"template_name": "settings/password_change.html",
         "password_change_form": CourtAdminPasswordChangeForm},
        name="password_change"),
    url(r"^settings/change-password/done/$", auth_views.password_change_done,
        {"template_name": "settings/password_change_done.html"},
        name="password_change_done"),
)
