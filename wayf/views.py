from models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    metadata = ShibbolethMetadata('metadata.xml')
    return HttpResponse("<br />".join(metadata.getIdpNames()))
