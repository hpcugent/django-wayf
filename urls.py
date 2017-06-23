from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve

urlpatterns = []


urlpatterns = [
  url(r'^static/(?P<path>.*)$', serve, {
    'document_root': settings.STATIC_ROOT
  }),
]
urlpatterns += [url(r'^(.*)', include('wayf.urls'))]
