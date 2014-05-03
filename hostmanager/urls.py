from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'registration/logout.html'}, 'auth_logout'),

    url(r'^accounts/password/change/$', 'django.contrib.auth.views.password_change',
        name='change-password'),
    url(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done',
       name='change-password-done'),
    url(r'^$', RedirectView.as_view(url='/sites/list/')),
    url(r'^sites/', include('manager.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('django.views.static',
            (r'^media/(?P<path>.*)$', 'serve',
                {'document_root': settings.MEDIA_ROOT}),)
