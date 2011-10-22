from grnet_aai.settings import WAYF_SITENAME
from django.http import HttpResponseServerError

class VhostMiddleware:
    def process_request(self,request):
        if 'HTTP_HOST' in request.META and \
            request.META['HTTP_HOST'] == WAYF_SITENAME:
            request.urlconf = 'grnet_aai.wayf.urls'

        return None


class HandleExceptionMiddleware:
    def process_exception(self, request, exception):
        if isinstance(exception, IOError) and \
           'request data read error' in unicode(exception):
            return HttpResponseServerError()
        return None
