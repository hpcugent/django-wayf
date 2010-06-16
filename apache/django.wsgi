# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

import os, sys
sys.path.append('/srv/www/aai.grnet.gr/')
sys.path.append('/srv/www/aai.grnet.gr/grnet_aai')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grnet_aai.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
