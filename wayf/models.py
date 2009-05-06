from xml.dom.minidom import parse

class ShibbolethMetadata:
    def __init__(self,filename):
        self.metadata = parse(filename)

    def getIdpNames(self):
        entities = self.metadata.getElementsByTagName('EntityDescriptor')
        idps = []
        for entity in entities:
            if entity.getElementsByTagName('IDPSSODescriptor'):
                idps.append(entity)
        return [ idp.getAttribute('entityID') for idp in idps ]


