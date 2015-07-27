from django.conf.urls import patterns, url

from . import views
from . import stateviews

urlpatterns = patterns(
    '',
    url(r'^urn_used/$', views.UrnAlreadyUsedView.as_view(), name='urn_already_used'),
    url(r'^new/(?P<stage>.+)/$', stateviews.state_view, name='state_form_step'),
    url(r'^(?P<stage>.+)/$', views.PleaOnlineViews.as_view(), name='plea_form_step'),
    url(r'^$', views.PleaOnlineViews.as_view(), name='plea_form'),
)
