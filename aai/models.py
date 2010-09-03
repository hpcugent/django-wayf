# -*- coding: utf-8 -*-
from lxml.objectify import parse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.utils.translation import get_language
import re


# A catalog of the institution categories. The order in which they appear
# here is the same as they will appear on the web.
institution_categories = (
      ('university', _l("Universities")),
      ('tei',  _l("Technological educational institutes")),
      ('ecclesiastical',  _l("Ecclesiastical schools")),
      ('school',  _l("Other academic institutions")),
      ('institute', _l("Research institutes")),
      ('other', _l("Other")),
      ('test', _l("Testing")),
)


class ShibbolethMetadata:
    """Basic object holding the shibboleth metadata"""

    def __init__(self,filename):
        """Initialize a ShibbolethMetadata object

        arguments:
            filename -- The location of the XML document containing Shibboleth metadata

        """

        self.metadata = parse(filename).getroot()

    def getIdps(self):
        """Returns an IdpList holding all Identity Providers found in the metadata"""
        def filtersso(entity):
            try:
                entity.IDPSSODescriptor
                return True
            except:
                return False

        # Create an IdpList holding all entities that contain an IDPSSODescriptor
        return IdpList([ IdentityProvider(kot) for kot in filter(filtersso, self.metadata.EntityDescriptor) ])


class IdpList(list):
    """Class holding a list of Shibboleth Identity Provides"""

    def __init__(self,idplist):
        """Create a new list of Identity Providers

        arguments:
            idplist -- a list of IdentityProvider instances

        """
        list.__init__(self,idplist)

    def __getitem__(self, key):
        # Allow for "idplist['a_provider_entityid'] lookups
        try:
            return filter(lambda x: x.id == key, self)[0]
        except:
            return None

    def getCategories(self):
        """Returns the list of known categories of Identity Providers"""

        return sorted(set(map(lambda x: x.getType(), self)))

    def getCategoryIdps(self, category):
        """Returns the list of known identity providers for a given category"""

        return filter(lambda x: x.getType() == category, self)

    def getIdpForScope(self, scope):
        """Returns the identity provider matching a given scope"""

        try:
            return filter(lambda x: x.matchesScope(scope), self)[0]
        except:
            return None

    def getIdpsByCategory(self, lang=None, exclude=None):
        """Returns a sequence of tuples of the form:
        
        (category, [ idp1, idp2, ...])
        
        where idpX is a dict { 'name': name, 'id': entityid }

        The list of idps is sorted by name

        """
        if not lang:
            lang = get_language()

        if exclude:
            validcats = filter(lambda x: x[0] not in exclude, institution_categories)
        else:
            validcats = institution_categories

        cats = map(lambda x: x[0], validcats) 

        categories = map(lambda x: { 'id': x[0], 'name': x[1] }, validcats)

        idps = []

        for category in cats:
            catidps = sorted(self.getCategoryIdps(category))
            idps.append(map(lambda x: {
                    'name': x.getName(lang),
                    'url': x.getURL(lang),
                    'id': x.id },
                    catidps))

        return zip(categories, idps)

class IdentityProvider:
    """Basic class holding a Shibboleth Identity Provider"""

    def __init__(self,idp):
        """Create a new IdentityProvider instance
        arguments:
            idp -- An lxml.objectify.Element holding an EntityDescriptor for a shibboleth IdP

        """

        self.idp = idp
        self.name = {} # Holds the institution's name in a form { language: string }
        self.url = {}
        self.id = self.idp.get('entityID')

        # Initialize the contact details
        self.contact = { 'givenName': '', 'surName': '', 'company': '', 'email': '', 'telephone': '', 'url': '' }

        # Dictionary to hold all SingleSignOnService definitions, by Binding
        self.sso = {}

        # Get the institution's name
        for name in self.idp.Organization.OrganizationDisplayName:
            self.name[name.get('{http://www.w3.org/XML/1998/namespace}lang')] = name.text

        for url in self.idp.Organization.OrganizationURL:
            self.url[url.get('{http://www.w3.org/XML/1998/namespace}lang')] = url.text

        # Fill in the contact details
        for contact in self.idp.ContactPerson:
            if contact.get('contactType') == "support":
                # We're not sure these details even exists, but since that would
                # require a set of nested checks, exception catching is more
                # clean.
                try:
                    self.contact['email'] = contact.EmailAddress.text
                except:
                    pass

                try:
                    self.contact['telephone'] = contact.TelephoneNumber.text
                except:
                    pass

        # Get all single-sign-on service descriptions
        for entry in self.idp.IDPSSODescriptor.SingleSignOnService:
            self.sso[entry.get('Binding')] = entry.get('Location')

    def __cmp__ (self,other):
        # Alphabetic sorting by name
        return cmp(self.getName(get_language()), other.getName(get_language()))

    def __repr__(self):
        return "IDP: \"" + self.name['en'] + '"'

    def getName(self,lang=None):
        if not lang:
            lang = get_language()

        try:
            return self.name[lang]
        except:
            return self.name['en']

    def getURL(self,lang=None):
        if not lang:
            lang = get_language()

        try:
            return self.url[lang]
        except:
            pass

        try:
            return self.url['en']
        except:
            pass

        return None

    def getType(self):
        """Returns the type (category) of the current IdP"""

        # Some heuristics to determine the IdP type, based on the 
        # institution's name in english.
        if self.name['en'].lower().find('university') >= 0:
            return "university"

        elif self.name['en'].lower().find('school of fine arts') >= 0:
            return "university"

        elif self.name['en'].lower().find('technological educational') >= 0:
            return "tei"

        if self.name['en'].lower().find('ecclesiastical') >= 0:
            return "ecclesiastical"

        elif re.findall(r'(school|academy)', self.name['en'].lower()):
            return "school"

        elif re.findall(r'(institute|cent(er|re))', self.name['en'].lower()):
            return "institute"

        if self.name['en'].lower().find('test') >= 0:
            return "test"

        else:
            return "other"
    
    def getScope(self):
        """Returns the scope of the current IdP"""

        scopes = filter(lambda x: x.tag == "{urn:mace:shibboleth:metadata:1.0}Scope", self.idp.IDPSSODescriptor.Extensions.getchildren())
        return scopes[0].text

    def matchesScope(self,scope):
        """Checks wheter the current IdPs scope matches the given string"""

        myscope = self.getScope()
        
        # Append a trailing '$', to align the regexp with the string end
        if myscope[-1] != '$':
            myscope += '$'

        if re.search(myscope, scope):
            return True

        return False
