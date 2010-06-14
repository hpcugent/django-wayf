from grnet_aai.settings import WAYF_SITENAME

class VhostMiddleware:
    def process_request(self,request):
        if 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == WAYF_SITENAME:
            request.urlconf = 'grnet_aai.wayf.urls'

        return None

