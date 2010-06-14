"""
A simple, translation-aware template loader from the application directories
It will try to load <template_name>.<language_code> and fall back to <template_name>.
"""

from django.utils import translation
from django.template import TemplateDoesNotExist
from django.template.loaders import filesystem
from django.conf import settings

def load_template_source(template_name, template_dirs=None):
    try:
        return filesystem.load_template_source(translation.get_language() + "/" + template_name, template_dirs)
    except TemplateDoesNotExist:
        pass

    try:
        return filesystem.load_template_source(settings.LANGUAGE_CODE + "/" + template_name, template_dirs)
    except TemplateDoesNotExist:
        pass

    return filesystem.load_template_source(template_name, template_dirs)

load_template_source.is_usable = True
