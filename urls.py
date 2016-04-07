from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = []


urlpatterns += patterns('', (r'^(.*)', include('wayf.urls')))

