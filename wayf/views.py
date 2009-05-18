from models import *
from util import *
from idpmap import *
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils.http import urlencode
from django.template.loader import render_to_string
from os import environ

def debug(request):
    return HttpResponse("<br />\n".join(map(lambda x: "%s: %s" % (x[0], x[1]), environ.items())))

def wayf_set(request):
    location = "/wayf"

    if 'queryString' in request.POST.keys():
        location += "?" + request.POST['queryString']

    response = HttpResponseRedirect(location)
 
    if 'user_idp' in request.POST.keys():
        if 'save' in request.POST.keys():
            if request.POST['save']:
                if request.POST['savetype'] == 'perm':
                    age = 86400 * 100 
                else:
                    age = None

        else:
            age = 5

        response.set_cookie(settings.IDP_COOKIE, request.POST['user_idp'], domain='.grnet.gr', max_age = age)

    return response

def wayf_unset(request):
    response = HttpResponseRedirect("/wayf")
    response.delete_cookie(settings.IDP_COOKIE, domain='.grnet.gr')
    return response

    
def wayf(request):
    # Instantiate the metadata
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)

    # Get the IdP list
    idps = metadata.getIdps()

    current_idp = None

    if settings.IDP_COOKIE in request.COOKIES.keys():
        current_idp = idps[request.COOKIES[settings.IDP_COOKIE]]

    if not current_idp:
        # Generate the category - idp list
        idplist = idps.getIdpsByCategory(request.LANGUAGE_CODE)

        # Render the wayf template
        return render_to_response("wayf.html", { 'idplist': idplist, 'request': request } )

    # Now we have an IdP. There are 2 cases:
    # 1. The request comes from an SP
    # 2. The request is stand-alone

    # Check if this is a Discovery Service request
    if 'entityID' in request.GET.keys():
        # Discovery Service mandates that 'entityID' holds the SP's ID
        if 'returnIDParam' in request.GET.keys() and request.GET['returnIDParam']:
            returnparam = request.GET['returnIDParam']
        else:
            returnparam = 'entityID'
        
        return HttpResponseRedirect(request.GET['return'] + "&" + urlencode(((returnparam, current_idp.id),)))

    # Check if this is an old Shibboleth 1.x request
    if 'shire' in request.GET.keys() and 'target' in request.GET.keys():
        # We just redirect the user to the given IdP
        return HttpResponseRedirect(
            current_idp.sso['urn:mace:shibboleth:1.0:profiles:AuthnRequest'] + "?" + request.GET.urlencode()
            )
    
    return render_to_response("wayf_set.html", { 'currentidp': current_idp.getName(request.LANGUAGE_CODE) })


def index(request):
    return render_to_response("index.html")

def support(request):
    # This gets triggered when a user's attributes fail to be accepted 
    # by a service provider. The aim is to produce a help page, indicating
    # the user's home institution contact details.

    opts = {}

    # Check to see whether _redirect_user_idp is set. This cookie will include
    # The user's selected IdP
    if settings.IDP_COOKIE in request.COOKIES.keys():
        userIdp = urldecode(request.COOKIES[settings.IDP_COOKIE])

        # Check to see if this is one of the old WAYF entries and map it to a
        # new entityID instead.
        if userIdp in idpmap.keys():
            userIdp = idpmap[userIdp]
            
        # Get the corresponding IdentityProvider instance
        idp = ShibbolethMetadata(settings.SHIB_METADATA).getIdps()[userIdp]

        if idp:
            opts['idp'] = idp
            opts['idpname'] = idp.getName(request.LANGUAGE_CODE)

    # At this point, no suitable IdentityProvider entry or one with no 
    # contact information was found. So, we have to apologise to the user.
    return render_to_response("support.html", opts)

def static(request):
    try:
        return render_to_response(request.path[1:] + ".html")
    except:
        return HttpResponseNotFound(render_to_string("404.html"))
