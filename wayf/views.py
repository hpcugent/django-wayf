from models import *
from util import *
from idpmap import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    # Get the user's preferred languages
    languages = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
    
    # Always include english at the end as a fall-back
    languages.append('en')

    # Instantiate the metadata
    metadata = ShibbolethMetadata('metadata.xml')

    # Render the wayf template
    return render_to_response("index.html", { 'idplist': metadata.getIdps().as_combo(languages)} )


def support(request):
    # This gets triggered when a user's attributes fail to be accepted 
    # by a service provider. The aim is to produce a help page, indicating
    # the user's home institution contact details.

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

        # If we got to this point with an IdP instance, then render the
        # support page template
        if idp:
            print idp.id
            return render_to_response("support.html", { 'idp': idp })

    # At this point, no suitable IdentityProvider entry was found. So, 
    # we have to apologise to the user.
    return render_to_response("support_fail.html")
