from django.urls import re_path
from wayf.views import wayf, setlanguage

urlpatterns = [
    re_path(r'^[/]?$', wayf),  # work around warning wrt url pattern starting with /
    re_path(r'^setlanguage/(.*)$', setlanguage),
]
