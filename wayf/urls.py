from django.conf.urls import url
from wayf.views import wayf, setlanguage

urlpatterns = []

urlpatterns += [
    url(r'^[/]?$', wayf),  # work around warning wrt url pattern starting with /
    url(r'^setlanguage/(.*)$', setlanguage),
]
