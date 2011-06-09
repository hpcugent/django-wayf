from aai.models import *
from aai.util import * 
import time 
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils.http import urlencode
from django.template.loader import render_to_string
from os import environ

def wayf(request):
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
    else:
        selectedidp = None

    # If this is the first visit, use some IP-based heuristics, as in utils.py's getUserRealm()
    if not selectedidp:
        selectedidp = idps.getIdpForScope(getUserRealm(request.META['REMOTE_ADDR']))

    # First check to see if anything has changed
    if request.method == "POST":
        if 'clear' in request.POST.keys():
            if request.POST['clear']:
                response = HttpResponseRedirect("/")
                response.delete_cookie(settings.IDP_COOKIE, domain=settings.COOKIE_DOMAIN)
                response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
                return response

        elif 'user_idp' in request.POST.keys():
            current_idp = idps[request.POST['user_idp']]
            if current_idp:
                selected_idp = current_idp
                cookies.append({'name': settings.LAST_IDP_COOKIE, 'data': request.POST['user_idp'], 'age': 86400 * 100})
                if request.POST.get('save'):
                    if request.POST.get('savetype') == 'perm':
                        age = 86400 * 100
                    else:
                        age = None
                    cookies.append({'name': settings.IDP_COOKIE, 'data': request.POST['user_idp'], 'age': age })

    # At this point we have handled the cookies and have an IdP, if the intent is such
    if not request.GET:
        # We were called without any arguments
        if current_idp:
            response = render_to_response("wayf_set.html", { 'currentidp': current_idp.getName() })
            for cookie in cookies:
                if cookie['age']:
                    expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + cookie['age']))
                else:
                    expires = None
                response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'], expires = expires)
        else:
            idplist = idps.getIdpsByCategory()
            response = render_to_response("wayf.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp })

        response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
        return response

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
            if cookie['age']:
                expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + cookie['age']))
            else:
                expires = None
            response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'], expires = expires)
        
        response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
        return response


    # If we got this far, then we need to be redirected, but don't know where to.
    # Let the user pick an IdP
    # Generate the category - idp list
    idplist = idps.getIdpsByCategory()

    # Render the apropriate wayf template
    response = render_to_response("wayf_from_sp.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp } )
    response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
    return response


