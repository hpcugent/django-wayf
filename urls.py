from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^support/?$', 'wayf.wayf.views.support'),
    (r'^help/?$', 'wayf.wayf.views.support',{ 'mode': 'help' }),
    (r'^debug/?$', 'wayf.wayf.views.debug'),
    (r'^/?$', 'wayf.wayf.views.index'),
    (r'^wayf/?$', 'wayf.wayf.views.wayf'),
    (r'^setlanguage/(.*)', 'wayf.wayf.views.setlanguage'),
    (r'.*', 'wayf.wayf.views.static'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
