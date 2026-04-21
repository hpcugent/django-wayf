import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wayf',
    version='0.3.10',
    packages=find_packages(),
    include_package_data=True,
    license='GPL v3',
    description='A simple Django implementation of a shibboleth/saml wayf service',
    long_description=README,
    url='https://github.com/hpcugent/django-wayf',
    author='Jens Timmerman',
    author_email='jens.timmerman@ugent.be',
    install_requires=[
        'lxml',
        'django >= 4.2, < 6',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
