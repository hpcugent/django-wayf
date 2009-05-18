from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^support$', 'wayf.views.support'),
    (r'^debug$', 'wayf.views.debug'),
    (r'^wayf$', 'wayf.views.wayf'),
    (r'^wayf/set$', 'wayf.views.wayf_set'),
    (r'^wayf/unset$', 'wayf.views.wayf_unset'),
    (r'^$', 'wayf.views.wayf'), 
    (r'.*', 'wayf.views.static'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
