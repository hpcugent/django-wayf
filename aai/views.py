import time

from os import environ

from aai.models import *
from aai.util import *
from grnet_aai.idpmap import *
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils.http import urlencode
from django.template.loader import render_to_string


def index(request):
    return render_to_response("index.html")

def idp_list(request):
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)
    idps = metadata.getIdps()
    idplist = idps.getIdpsByCategory(exclude=('wayf', 'test'))

    return render_to_response("idp_list.html", { 'idplist' : idplist } )

def static(request):
    # A catch-all view, trying to render all our static pages or give a 404 
    try:
        return render_to_response(request.path[1:] + ".html")
    except:
        return HttpResponseNotFound(render_to_string("404.html"))

def support(request, mode="support"):
    # This gets triggered when a user's attributes fail to be accepted 
    # by a service provider. The aim is to produce a help page, indicating
    # the user's home institution contact details.

    opts = {}
    userIdp = None

    # Check to see whether _redirect_user_idp is set. This cookie will include
    # The user's selected IdP
    if settings.IDP_COOKIE in request.COOKIES.keys():
        userIdp = urldecode(request.COOKIES[settings.IDP_COOKIE])
    elif settings.LAST_IDP_COOKIE in request.COOKIES.keys():
        userIdp = urldecode(request.COOKIES[settings.LAST_IDP_COOKIE])

    if userIdp:
        # Check to see if this is one of the old WAYF entries and map it to a
        # new entityID instead.
        if userIdp in idpmap.keys():
            userIdp = idpmap[userIdp]
            
        # Get the corresponding IdentityProvider instance
        idp = ShibbolethMetadata(settings.SHIB_METADATA).getIdps()[userIdp]

        if idp:
            opts['idp'] = idp
            opts['idpname'] = idp.getName()

    if mode == "help":
        response = render_to_response("help.html", opts)
    else:
        response = render_to_response("support.html", opts)

    response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
    return response

def setlanguage(request, lang):
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang, domain='.grnet.gr', max_age = 100 * 86400, expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + 100 * 86400)))
    response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
    return response

def debug(request):
    return HttpResponse("<br />\n".join(map(lambda x: "%s: %s" % (x[0], x[1]), environ.items())))

