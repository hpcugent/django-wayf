from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = []

# Static files
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 'serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^favicon.ico$', 'serve',
        {'path': "favicon.ico"}),
    (r'^robots.txt$', 'serve',
        {'path': "robots.txt"}),
    )

urlpatterns += patterns('',
    (r'^/?$', 'grnet_aai.wayf.views.wayf'),
    (r'^setlanguage/(.*)', 'grnet_aai.aai.views.setlanguage'),
)
