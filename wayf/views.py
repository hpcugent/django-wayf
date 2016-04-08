from wayf.utils import ShibbolethMetadata
# optional for now , getUserRealm
import time
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.template import RequestContext


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
    # this uses the getUserRealm magic from dnsutils
    #if not selectedidp:
    #    selectedidp = idps.getIdpForScope(getUserRealm(request.META['REMOTE_ADDR']))

    # First check to see if anything has changed
    if request.method == "POST":
        if 'clear' in request.POST.keys():
            if request.POST['clear']:
                response = HttpResponseRedirect("/")
                response.delete_cookie(settings.IDP_COOKIE, domain=settings.COOKIE_DOMAIN)
                response['P3P'] = settings.P3P_HEADER
                return response

        elif 'user_idp' in request.POST.keys():
            current_idp = idps[request.POST['user_idp']]
            if current_idp:
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
            response = render_to_response("wayf_set.html", { 'currentidp': current_idp.getName() }, context_instance=RequestContext(request))
            for cookie in cookies:
                if cookie['age']:
                    expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + cookie['age']))
                else:
                    expires = None
                response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'], expires = expires)
        else:
            idplist = idps.getIdpsByCategory()
            response = render_to_response("wayf.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp }, context_instance=RequestContext(request))

        response['P3P'] = settings.P3P_HEADER
        return response

    # If we got to this point, then this is a request comming from an SP
    if current_idp:
        # We have an IdP to route the request to
        if 'entityID' in request.GET.keys() and 'return' in request.GET.keys():
            # a SAML Discovery Service request
            # Discovery Service mandates that 'entityID' holds the SP's ID
            if 'returnIDParam' in request.GET.keys() and request.GET['returnIDParam']:
                returnparam = request.GET['returnIDParam']
            else:
                returnparam = 'entityID'

            response = HttpResponseRedirect(request.GET['return'] + "&" + urlencode(((returnparam, current_idp.id),)))
        elif 'shire' in request.GET.keys() and 'target' in request.GET.keys():
            # an old Shibboleth 1.x request
            # We just redirect the user to the given IdP
            response = HttpResponseRedirect(
                current_idp.sso['urn:mace:shibboleth:1.0:profiles:AuthnRequest'] + "?" + request.GET.urlencode()
                )
        else:
            response = render_to_response("500.html")
            response.status_code = 400 # bad request

        for cookie in cookies:
            if cookie['age']:
                expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + cookie['age']))
            else:
                expires = None
            response.set_cookie(cookie['name'], cookie['data'], domain=settings.COOKIE_DOMAIN, max_age=cookie['age'], expires = expires)

        response['P3P'] = settings.P3P_HEADER
        return response


    # If we got this far, then we need to be redirected, but don't know where to.
    # Let the user pick an IdP
    # Generate the category - idp list
    idplist = idps.getIdpsByCategory()

    # Render the apropriate wayf template
    response = render_to_response("wayf_from_sp.html", { 'idplist': idplist, 'request': request, 'selected': selectedidp }, context_instance=RequestContext(request) )
    response['P3P'] = settings.P3P_HEADER
    return response

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def idp_list(request):
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)
    idps = metadata.getIdps()
    idplist = idps.getIdpsByCategory(exclude=('wayf', 'test'))

    return render_to_response("idp_list.html", { 'idplist' : idplist }, context_instance=RequestContext(request) )

def sp_list(request):
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)
    sps = metadata.getSps()
    splist = sps.getEntitiesByGroup()
    # splist_other = entities in the top group
    splist_other = [i[1] for i in splist if i[0] == 'http://www.grnet.gr/aai'][0]
    # fitlerids = entity.id for entities not in the top group
    filterids = [o['id'] for i in splist for o in i[1] if i[0] != 'http://www.grnet.gr/aai']
    # filter out entities not in the top group from splist_other
    splist_other_new = filter(lambda x: x['id'] not in filterids, splist_other)
    # replace top group with filtered out version in splist
    splist.insert(splist.index(('http://www.grnet.gr/aai', splist_other)), ('other', splist_other_new))
    splist.remove(('http://www.grnet.gr/aai', splist_other))

    return render_to_response("sp_list.html", { 'splist' : splist }, context_instance=RequestContext(request) )

def entity_list(request, group = None):
    if group is not None:
        group = "http://aai.grnet.gr%s" % request.path_info
    metadata = ShibbolethMetadata(settings.SHIB_METADATA)
    entities = metadata.getEntities(augmented=True)
    entlist = entities.getEntities(group=group, logosize=(100,100))

    return render_to_response("entity_list.html", { 'entlist' : entlist,
                                                    'group' : group } , context_instance=RequestContext(request))

""" example support view
uses urldecode from dnsutils
and needs an idpmap from somewhere
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
        response = render_to_response("help.html", opts, context_instance=RequestContext(request))
    else:
        response = render_to_response("support.html", opts, context_instance=RequestContext(request))

    response['P3P'] = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
    return response
"""

def setlanguage(request, lang):
    try:
        url = request.META['HTTP_REFERER']
    except KeyError:
        url = '/'

    response = HttpResponseRedirect(url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang, domain=settings.COOKIE_DOMAIN, max_age = 100 * 86400, expires = time.strftime("%a, %d-%m-%y %H:%M:%S GMT", time.gmtime(time.time() + 100 * 86400)))
    response['P3P'] = settings.P3P_HEADER
    return response
