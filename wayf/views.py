from models import *
from util import *
from idpmap import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    languages = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
    languages.append('en')
    metadata = ShibbolethMetadata('metadata.xml')
    return render_to_response("index.html", { 'idplist': metadata.getIdps().as_combo(languages)} )

def support(request):
    if '_redirect_user_idp' in request.COOKIES.keys():
        userIdp = urldecode(request.COOKIES['_redirect_user_idp'])
        if userIdp in idpmap.keys():
            userIdp = idpmap[userIdp]
        idp = ShibbolethMetadata('metadata.xml').getIdps()[userIdp]
        if idp:
            print idp.id
            return render_to_response("support.html", { 'idp': idp })

    return render_to_response("support_fail.html")
