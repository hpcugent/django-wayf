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

if settings.DEBUG:
    urlpatterns += patterns('', (r'^wayf/(.*)', include('grnet_aai.wayf.urls')))

urlpatterns += patterns('',
    (r'^support/?$', 'grnet_aai.aai.views.support'),
    (r'^help/?$', 'grnet_aai.aai.views.support',{ 'mode': 'help' }),
    (r'^debug/?$', 'grnet_aai.aai.views.debug'),
    (r'^setlanguage/(.*)', 'grnet_aai.aai.views.setlanguage'),
    (r'^participants/?$', 'grnet_aai.aai.views.idp_list'),
    (r'^service-providers/?$', 'grnet_aai.aai.views.sp_list'),
    (r'^entities/?(.+)?$', 'grnet_aai.aai.views.entity_list'),
    (r'^(registry/.+)/$', 'grnet_aai.aai.views.static'),
    (r'^feeds/(.+\.json)$', 'grnet_aai.aai.views.json'),
    (r'^/?$', 'grnet_aai.aai.views.index'),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^schema/(?P<schema>.+)/$', 'redirect_to',
        {'url': '/static/%(schema)s.schema', 'permanent': False}),
    (r'^schemas/(?P<schema>.+)/$', 'redirect_to',
        {'url': '/static/%(schema)s.schema', 'permanent': False}),
    (r'^policy/$', 'redirect_to',
        {'url': '/documentation/', 'permanent': False}),
    (r'^policy/(?P<filename>.+)$', 'redirect_to',
        {'url': '/static/policy/%(filename)s', 'permanent': False}),
)

# catch-all
urlpatterns += patterns('',
    (r'([^/]+)/?$', 'grnet_aai.aai.views.static'),
)
