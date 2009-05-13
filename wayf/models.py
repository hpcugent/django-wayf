# -*- coding: utf-8 -*-
from lxml.objectify import parse
import re


institution_categories = (
      ('university', { 'en': 'Universities', 'el': u'Πανεπιστήμια' }),
      ('tei', { 'en': 'Technological Educational Institutes', 'el': u'Τεχνολογικά Εκπαιδευτικά Ιδρύματα' }),
      ('institute', { 'en': 'Research Institutes', 'el': u'Ερευνητικά ινστιτούτα' }),
      ('other', { 'en': 'Other', 'el': u'Άλλα' }),
      ('test', { 'en': 'Testing', 'el': u'Δοκιμαστικοί φορείς' }),
      ('wayf', { 'en': 'Other federations', 'el': u'Άλλες ομοσπονδίες' }),
)


class ShibbolethMetadata:
    def __init__(self,filename):
        self.metadata = parse(filename).getroot()

    def getIdps(self):
        def filtersso(entity):
            try:
                entity.IDPSSODescriptor
                return True
            except:
                return False
        return IdpList([ IdentityProvider(kot) for kot in filter(filtersso, self.metadata.EntityDescriptor) ])

class IdpList(list):
    def __init__(self,idplist):
        list.__init__(self,idplist)

    def __getitem__(self, key):
        try:
            return filter(lambda x: x.id == key, self)[0]
        except:
            return None

    def getCategories(self):
        return sorted(set(map(lambda x: x.getType(), self)))

    def getCategoryIdps(self, category):
        return filter(lambda x: x.getType() == category, self)

    def getIdpForScope(self, scope):
        try:
            return filter(lambda x: x.matchesScope(scope), self)[0]
        except:
            return None

    def as_combo(self,languages=[]):
        string = '<select name="user_idp">\n'
        for category, catnames in institution_categories:
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
    def __init__(self,idp):

        self.idp = idp
        self.name = {}
        self.id = self.idp.get('entityID')
        self.contact = { 'givenName': '', 'surName': '', 'company': '', 'email': '', 'telephone': '', 'url': '' }
        self.sso = {}

        for name in self.idp.Organization.OrganizationDisplayName:
            self.name[name.get('{http://www.w3.org/XML/1998/namespace}lang')] = name.text

        for contact in self.idp.ContactPerson:
            if contact.get('contactType') == "support":
                try:
                    self.contact['email'] = contact.EmailAddress.text
                except:
                    pass
                try:
                    self.contact['telephone'] = contact.TelephoneNumber.text
                except:
                    pass

        for entry in self.idp.IDPSSODescriptor.SingleSignOnService:
            self.sso[entry.get('Binding')] = entry.get('Location')

    def __repr__(self):
        return "IDP: \"" + self.name['en'] + '"'

    def getType(self):
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
        scopes = filter(lambda x: x.tag == "{urn:mace:shibboleth:metadata:1.0}Scope", self.idp.IDPSSODescriptor.Extensions.getchildren())
        return scopes[0].text

    def matchesScope(self,scope):
        myscope = self.getScope()
        if myscope[-1] != '$':
            myscope += '$'
        if re.search(myscope, scope):
            return True
        return False
