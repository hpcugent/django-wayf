from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = []


urlpatterns = patterns('',
  url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_ROOT}
        ),
)
urlpatterns += patterns('', (r'^(.*)', include('wayf.urls')))
