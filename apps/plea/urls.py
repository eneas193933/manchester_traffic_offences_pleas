from django.conf.urls import patterns, url

from . import views
from . import stateviews

urlpatterns = patterns(
    '',
    url(r'^urn_used/$', views.UrnAlreadyUsedView.as_view(), name='urn_already_used'),
    url(r'^new/(?P<state>.+)/(?P<index>[0-9]{1,2})/$', stateviews.state_view, name='plea_form_step'),
    url(r'^new/(?P<state>.+)/$', stateviews.state_view, name='state_form_step'),
    url(r'^(?P<stage>.+)/$', views.PleaOnlineViews.as_view(), name='plea_form_step'),
    url(r'^$', views.PleaOnlineViews.as_view(), name='plea_form'),
)
