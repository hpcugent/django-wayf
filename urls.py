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

if settings.DEBUG:
    urlpatterns += patterns('', (r'^wayf/(.*)', include('wayf.urls')))

urlpatterns += patterns('',
    (r'^support/?$', 'aai.views.support'),
    (r'^help/?$', 'aai.views.support',{ 'mode': 'help' }),
    (r'^debug/?$', 'aai.views.debug'),
    (r'^setlanguage/(.*)', 'aai.views.setlanguage'),
    (r'^participants/?$', 'aai.views.idp_list'),
    (r'^service-providers/?$', 'aai.views.sp_list'),
    (r'^entities/?(.+)?$', 'aai.views.entity_list'),
    (r'^(registry/.+)/$', 'aai.views.static'),
    (r'^feeds/(.+\.json)$', 'aai.views.json'),
    (r'^/?$', 'aai.views.index'),
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
    (r'([^/]+)/?$', 'aai.views.static'),
)
