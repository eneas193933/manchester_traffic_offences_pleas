# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

import views

handler500 = "manchester_traffic_offences.views.server_error"

urlpatterns = patterns('',
                       url(r'^$', views.HomeView.as_view(), name="home"),
                       url(r'^terms-and-conditions-and-privacy-policy$',
                           TemplateView.as_view(template_name="terms.html"),
                           name="terms"),
                       url(r'^plea/', include('apps.plea.urls', )),
                       url(r'^feedback/', include('apps.feedback.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
