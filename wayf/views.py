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

def wayf(request):
    print request.POST.items()
    # Instantiate the metadata
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)

    # Get the IdP list
    idps = metadata.getIdps()

    # A list to hold the cookies-to-be-set
    cookies = []

    # Get the current IdP, if there is one
    if settings.IDP_COOKIE in request.COOKIES.keys():
        current_idp = idps[request.COOKIES[settings.IDP_COOKIE]]
    else:
        current_idp = None

    # Try to get the user's last used IdP
    if settings.LAST_IDP_COOKIE in request.COOKIES.keys():
        selectedidp = idps[request.COOKIES[settings.LAST_IDP_COOKIE]]

    # If this is the first visit, use some IP-based heuristics, as in utils.py's getUserRealm()
    if not selectedidp:
        selectedidp = idps.getIdpForScope(getUserRealm(request.META['HTTP_X_FORWARDED_FOR']))

    # First check to see if anything has changed
    if request.method == "POST":
        if 'clear' in request.POST.keys():
            if request.POST['clear']:
                response = HttpResponseRedirect("/")
                response.delete_cookie(settings.IDP_COOKIE, domain=settings.COOKIE_DOMAIN)
                print response
                return response

        elif 'user_idp' in request.POST.keys():
            current_idp = idps[request.POST['user_idp']]
            if current_idp:
                selected_idp = current_idp
                cookies.append({'name': settings.LAST_IDP_COOKIE, 'data': request.POST['user_idp'], 'age': 86400 * 100})
                if 'save' in request.POST.keys():
                    if request.POST['save']:
                        if request.POST['savetype'] == 'perm':
                            age = 86400 * 100 
                        else:
                            age = None
                    cookies.append({'name': settings.IDP_COOKIE, 'data': request.POST['user_idp'], 'age': age })
    
    # At this point we have handled the cookies and have an IdP, if the intent is such
    if not request.GET:
        # We were called without any arguments
        if current_idp:
            response = render_to_response("wayf_set.html", { 'currentidp': current_idp.getName(request.LANGUAGE_CODE) })
            for cookie in cookies:
                response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'])
            return response
        else:
            idplist = idps.getIdpsByCategory(request.LANGUAGE_CODE)

            return render_to_response("wayf.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp })

    # If we got to this point, then this is a request comming from an SP
    if current_idp:
        # We have an IdP to route the request to
        # Check if this is a Discovery Service request
        if 'entityID' in request.GET.keys():
            # Discovery Service mandates that 'entityID' holds the SP's ID
            if 'returnIDParam' in request.GET.keys() and request.GET['returnIDParam']:
                returnparam = request.GET['returnIDParam']
            else:
                returnparam = 'entityID'
            
            response = HttpResponseRedirect(request.GET['return'] + "&" + urlencode(((returnparam, current_idp.id),)))

        # Check if this is an old Shibboleth 1.x request
        elif 'shire' in request.GET.keys() and 'target' in request.GET.keys():
            # We just redirect the user to the given IdP
            response = HttpResponseRedirect(
                current_idp.sso['urn:mace:shibboleth:1.0:profiles:AuthnRequest'] + "?" + request.GET.urlencode()
                )

        else:
            response = render_to_response("bad.html")

        for cookie in cookies:
            response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'])
        
        return response


    # If we got this far, then we need to be redirected, but don't know where to.
    # Let the user pick an IdP
    # Generate the category - idp list
    idplist = idps.getIdpsByCategory(request.LANGUAGE_CODE)


    # Render the apropriate wayf template
    return render_to_response("wayf.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp } )


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
    # A catch-all view, trying to render all our static pages or give a 404 
    try:
        return render_to_response(request.path[1:] + ".html")
    except:
        return HttpResponseNotFound(render_to_string("404.html"))
