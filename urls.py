from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^support/?$', 'grnet_aai.aai.views.support'),
    (r'^help/?$', 'grnet_aai.aai.views.support',{ 'mode': 'help' }),
    (r'^debug/?$', 'grnet_aai.aai.views.debug'),
    (r'^setlanguage/(.*)', 'grnet_aai.aai.views.setlanguage'),
    (r'^participants/?$', 'grnet_aai.aai.views.idp_list'),
    (r'^/?$', 'grnet_aai.aai.views.index'),
    (r'.*', 'grnet_aai.aai.views.static'),
)
