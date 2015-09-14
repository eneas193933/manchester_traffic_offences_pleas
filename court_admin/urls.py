from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf import settings

from views import UsageStatsView


urlpatterns = patterns("",
    (r'^$', UsageStatsView.as_view()),
    (r'^', include('registration.backends.default.urls')),)


