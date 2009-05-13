# -*- coding: utf-8 -*-
from lxml.objectify import parse
import re


# A catalog of the institution categories. The order in which they appear
# here is the same as they will appear on the web.
institution_categories = (
      ('university', { 'en': 'Universities', 'el': u'Πανεπιστήμια' }),
      ('tei', { 'en': 'Technological Educational Institutes', 'el': u'Τεχνολογικά Εκπαιδευτικά Ιδρύματα' }),
      ('institute', { 'en': 'Research Institutes', 'el': u'Ερευνητικά ινστιτούτα' }),
      ('other', { 'en': 'Other', 'el': u'Άλλα' }),
      ('test', { 'en': 'Testing', 'el': u'Δοκιμαστικοί φορείς' }),
      ('wayf', { 'en': 'Other federations', 'el': u'Άλλες ομοσπονδίες' }),
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

    def as_combo(self,languages=["en"]):
        """Returns an HTML string with  a combo box definition for all identity providers, sorted by category.
        arguments:
            languages -- An array of languages, in desceding order of preference

        """

        string = '<select name="user_idp">\n'
        for category, catnames in institution_categories:
            # Check for languages, in descending order of preference
            for language in languages:
                if language in catnames.keys():
                    string += "    <optgroup label='%s'>\n" % unicode(catnames[language])
                    break

            for idp in sorted(self.getCategoryIdps(category)):
                for language in languages:
                    if language in idp.name.keys():
                        string += "        <option value=\"%s\">%s</option>\n" % (idp.id, unicode(idp.name[language]))
                        break
            string += "    </optgroup>\n"
        string += "</select>\n"
        return string


class IdentityProvider:
    """Basic class holding a Shibboleth Identity Provider"""

    def __init__(self,idp):
        """Create a new IdentityProvider instance
        arguments:
            idp -- An lxml.objectify.Element holding an EntityDescriptor for a shibboleth IdP

        """

        self.idp = idp
        self.name = {} # Holds the institution's name in a form { language: string }
        self.id = self.idp.get('entityID')

        # Initialize the contact details
        self.contact = { 'givenName': '', 'surName': '', 'company': '', 'email': '', 'telephone': '', 'url': '' }

        # Dictionary to hold all SingleSignOnService definitions, by Binding
        self.sso = {}

        # Get the institution's name
        for name in self.idp.Organization.OrganizationDisplayName:
            self.name[name.get('{http://www.w3.org/XML/1998/namespace}lang')] = name.text

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

    def __repr__(self):
        return "IDP: \"" + self.name['en'] + '"'

    def getType(self):
        """Returns the type (category) of the current IdP"""

        # Some heuristics to determine the IdP type, based on the 
        # institution's name in english.
        if self.name['en'].lower().find('edugain') >= 0:
            return "wayf"

        elif self.name['en'].lower().find('university') >= 0:
            return "university"

        elif self.name['en'].lower().find('technological educational') >= 0:
            return "tei"

        elif re.findall(r'(institute|cent(er|re))', self.name['en'].lower()):
            return "institute"

        elif re.findall(r'(test|service box)', self.name['en'].lower()):
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
