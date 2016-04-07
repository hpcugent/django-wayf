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

2. Include the wayf URLconf in your project urls.py like this::

    url(r'^wayf', include('wayf.urls')),

   If you want more flexibility around the templates,
   there is only one view  for the basic app
   wayf.views.wayf
   so you can create your own url that points to just this view.
   TODO: more flexibility towards the templates it uses.

3. This app doesn't store anything in it's models, so no migrations are needed

4. Start the development server and visit http://127.0.0.1:8000/wayf
   To select your home institute

5. Redirect a service here so

dependencies
---

This suite requires the following python modules to be present on the system:

   - python-lxml: uses lxml.objectify to parse the XML metadata
optional, not fully implemented yet, you will need to manually make some changes:
   - pydns: used for reverse DNS lookup to get a hint about a user's preferred IdP
   - IPy: used for IP map manipulation

