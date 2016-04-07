"""
A simple, translation-aware template loader from the application directories
It will try to load <template_name>.<language_code> and fall back to <template_name>.
"""

from django.utils import translation
from django.template import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as BaseLoader
from django.conf import settings


class Loader(BaseLoader):

    def load_template_source(self, template_name, template_dirs=None):
        try:
            return BaseLoader.load_template_source(self, translation.get_language() + "/" + template_name, template_dirs)
        except TemplateDoesNotExist:
            pass

        try:
            return BaseLoader.load_template_source(self, settings.LANGUAGE_CODE + "/" + template_name, template_dirs)
        except TemplateDoesNotExist:
            pass

        return BaseLoader.load_template_source(self, template_name, template_dirs)

    load_template_source.is_usable = True
