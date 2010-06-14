from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^support/?$', 'grnet_aai.aai.views.support'),
    (r'^help/?$', 'grnet_aai.aai.views.support',{ 'mode': 'help' }),
    (r'^/?$', 'grnet_aai.wayf.views.wayf'),
    (r'^setlanguage/(.*)', 'grnet_aai.aai.views.setlanguage'),
)
