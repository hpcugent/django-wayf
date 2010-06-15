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
    (r'^support/?$', 'grnet_aai.aai.views.support'),
    (r'^help/?$', 'grnet_aai.aai.views.support',{ 'mode': 'help' }),
    (r'^debug/?$', 'grnet_aai.aai.views.debug'),
    (r'^setlanguage/(.*)', 'grnet_aai.aai.views.setlanguage'),
    (r'^participants/?$', 'grnet_aai.aai.views.idp_list'),
    (r'^/?$', 'grnet_aai.aai.views.index'),
    (r'([^/]+)/?$', 'grnet_aai.aai.views.static'),
)

