from models import *
from util import *
from idpmap import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

IDP_COOKIE = 'grnet_selected_idp'

def debug(request):
    return HttpResponse("<br />\n".join(map(lambda x: "%s: %s" % (x[0], x[1]), request.COOKIES.items())))

def wayf_set(request):
    response = HttpResponseRedirect("/wayf")

    if 'user_idp' in request.POST.keys():
        response.set_cookie(IDP_COOKIE, request.POST['user_idp'], domain='.grnet.gr')

    return response

def wayf_unset(request):
    response = HttpResponseRedirect("/wayf")
    response.delete_cookie(IDP_COOKIE, domain='.grnet.gr')
    return response

    
def wayf(request):
    # Instantiate the metadata
    metadata = ShibbolethMetadata('metadata.xml')

    # Get the IdP list
    idps = metadata.getIdps()

    if IDP_COOKIE in request.COOKIES.keys():
        current_idp = idps[request.COOKIES[IDP_COOKIE]].getName(request.LANGUAGE_CODE)
        try:
            return render_to_response("wayf_set.html." + request.LANGUAGE_CODE, { 'currentidp': current_idp })
        except:
            return render_to_response("wayf_set.html", { 'currentidp': current_idp })

    # List the categories and their titles
    cats = map(lambda x: x[0], institution_categories)
    cattitles = map(lambda x: x[1], institution_categories)

    # Generate the category - idp list
    # Black voodoo - functional magic
    idplist = zip(
        cattitles, 
        map(
            lambda x: map(
                lambda y: {'name': y.getName(request.LANGUAGE_CODE), 'id': y.id },
                sorted(
                    idps.getCategoryIdps(x), lambda z,w: cmp(z.getName(request.LANGUAGE_CODE), w.getName(request.LANGUAGE_CODE))
                )
            ), 
            cats
        )
    )

    # Render the wayf template
    try:
        return render_to_response("wayf.html." + request.LANGUAGE_CODE, { 'idplist': idplist } )
    except:
        return render_to_response("wayf.html", { 'idplist': idplist } )


def index(request):
    return render_to_response("index.html")


def support(request):
    # This gets triggered when a user's attributes fail to be accepted 
    # by a service provider. The aim is to produce a help page, indicating
    # the user's home institution contact details.

    idpname = ''

    # Check to see whether _redirect_user_idp is set. This cookie will include
    # The user's selected IdP
    if '_redirect_user_idp' in request.COOKIES.keys():
        userIdp = urldecode(request.COOKIES['_redirect_user_idp'])

        # Check to see if this is one of the old WAYF entries and map it to a
        # new entityID instead.
        if userIdp in idpmap.keys():
            userIdp = idpmap[userIdp]
            
        # Get the corresponding IdentityProvider instance
        idp = ShibbolethMetadata('metadata.xml').getIdps()[userIdp]

        if idp:
            try:
                idpname = idp.name[request.LANGUAGE_CODE]
            except:
                idpname = idp.name['en']
            if idp.contact['telephone'] or idp.contact['email']:
                # If we got to this point with an IdP instance, then render the
                # support page template
                return render_to_response("support.html", { 'idp': idp, 'idpname': idpname })

    # At this point, no suitable IdentityProvider entry or one with no 
    # contact information was found. So, we have to apologise to the user.
    return render_to_response("support_fail.html", { 'idpname': idpname })

def faq(request):
    return render_to_response("faq.html")

def help(request):
    return render_to_response("help.html")

def privacy(request):
    return render_to_response("privacy.html")
