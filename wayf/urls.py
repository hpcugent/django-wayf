from django.conf import settings
from django.conf.urls import patterns, url, include

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
    (r'^/?$', 'wayf.views.wayf'),
    (r'^setlanguage/(.*)', 'aai.views.setlanguage'),
    (r'^feeds/(.+\.json)$', 'aai.views.json'),
)
