from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('manager.views',
    url(r'^$', RedirectView.as_view(url='/sites/list/'), name='manager-index'),
    url(r'^list/$', 'site_list', name='site-list'),
    url(r'^add/$', 'add_site', name='create-host'),
    url(r'^delete/(?P<host_id>\d+)/$', 'delete_host', name='delete-host'),
    url(r'^get/(?P<host_id>\d+)/$', 'get_site_info'),
    url(r'^site/change/$', 'change_host', name='change-host'),
)
