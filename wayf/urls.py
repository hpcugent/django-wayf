from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = []

urlpatterns += patterns('',
    (r'^/?$', 'wayf.views.wayf'),
    (r'^setlanguage/(.*)', 'wayf.views.setlanguage'),
)
