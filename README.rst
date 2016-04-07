=====
WAYF
=====

WAYF is a simple Django app that implements a SAML WAYF (Where Are You From) service.
It allows you to select your home idP (institute) for further redirection,
by parsing your federation metadata(.xml)

This code originates from https://code.grnet.gr/projects/wayf

it was adapted to split of the wayf part as a separate usable django app


Quick start
-----------

1. Add "wayf" to your INSTALLED_APPS setting  and configure the location of your metadata like this::

    INSTALLED_APPS = [
        ...
        'wayf',
    ]
    SHIB_METADATA = 'federation-metadata.xml'
    INSTITUTION_CATEGORIES = (
      ('university', ("Universities")),
      ('tei',  ("Technological educational institutes")),
      ('school',  ("Other academic institutions")),
      ('institute', ("Research institutes")),
      ('other', ("Please select your institute")),
      ('test', ("Testing")),
    )
    P3P_HEADER = ''
    IDP_COOKIE = 'wayf_selected_idp'
    LAST_IDP_COOKIE = 'wayf_last_idp'
    COOKIE_DOMAIN = '.example.com'

2. Include the wayf URLconf in your project urls.py like this::

    url(r'^wayf', include('wayf.urls')),

   If you want more flexibility around the templates,
   there is only one view  for the basic app
   wayf.views.wayf
   so you can create your own url that points to just this view.
   The templates shipped with wayf extend a base.html template, where they will insert their html in the {% content %} tag.


3. This app doesn't store anything in it's models, so no migrations are needed

4. Start the development server and visit http://127.0.0.1:8000/wayf
   To select your home institute

5. Configure your shibboleth2.xml file to use this wayf::
   <SessionInitiator type="Chaining" Location="/DS" id="DS"  isDefault="true" relayState="cookie">
                <SessionInitiator type="SAMLDS" URL="https://example.com/wayf"/>
   <SessionInitiator/>


extra
---
The only view you really need is wayf.views.wayf

however, wayf.views contains a few other views, that can help you generate auto generated pages
for users, e.g. using templates like::

    If you encountered a problem <b>in your Home Organization's authentication page</b>, then you should contact your Home Organization's User Helpdesk. This is also the place to s    olve account-related issues, like the loss or change of your password, change of your contact details, etc.
    {% if idp.contact.email or idp.contact.telephone %}
    According to your selected Home Organization, &quot;<b>{{ idpname }}</b>&quot;, you may use the following contact details for getting support:
    <ul id="contactdetails">
    {% if idp.contact.email  %}
            <li><strong>E-mail:</strong> <a href="mailto:{{ idp.contact.email }}?subject=AAI+issue+report">{{ idp.contact.email }}</a></li>
    {% endif %}
    {% if idp.contact.telephone %}
            <li><strong>{% trans "Telephone" %}:</strong> {{ idp.contact.telephone }}</li>
    {% endif %}
    </ul>
    {% endif %}</li>


dependencies
---

This suite requires the following python modules to be present on the system:

   - python-lxml: uses lxml.objectify to parse the XML metadata
optional, not fully implemented yet, you will need to manually make some changes:
   - pydns: used for reverse DNS lookup to get a hint about a user's preferred IdP
   - IPy: used for IP map manipulation

