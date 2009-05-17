from django.utils import translation
from django.template.loaders import app_directories

def load_template_source(template_name, template_dirs=None):
    try:
        return app_directories.load_template_source(template_name + "." + translation.get_language(), template_dirs)
    except:
        return app_directories.load_template_source(template_name, template_dirs)

load_template_source.is_usable = True
