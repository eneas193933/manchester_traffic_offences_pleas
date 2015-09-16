from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse

from .admin import court_admin
from views import UsageStatsView


urlpatterns = patterns("",
    url(r"^$", UsageStatsView.as_view(),
        name="usage_stats"),

    url(r"^admin/", include(court_admin.urls)),

    # django auth views
    url(r'^login/$', auth_views.login,
        {'template_name': 'court_admin/login.html'},
        name='login'),

    url(r'^logout/$', auth_views.logout_then_login,
        {"login_url": "/court-admin/login/"},
        name='logout'),

    url(r'^password-change/$', auth_views.password_change,
        {'template_name': 'court_admin/password_change_form.html'},
        name='password_change'),

    url(r'^password-change/done/$', auth_views.password_change_done,
        {'template_name': 'court_admin/password_change_done.html'},
        name='password_change_done'),

    url(r'^password-reset/$', auth_views.password_reset,
        {'template_name': 'court_admin/password_reset_form.html',
         'email_template_name': 'court_admin/password_reset_email.html',
         'subject_template_name': 'court_admin/password_reset_subject.txt'},
        name='password_reset'),

    url(r'^password-reset/done/$', auth_views.password_reset_done,
        {'template_name': 'court_admin/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'court_admin/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'court_admin/password_reset_complete.html'},
        name='password_reset_complete'),
)