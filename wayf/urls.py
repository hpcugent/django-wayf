from django.conf.urls import url
from wayf.views import wayf, setlanguage

urlpatterns = []

urlpatterns += [
    url(r'^/?$', wayf),
    url(r'^setlanguage/(.*)', setlanguage),
]
