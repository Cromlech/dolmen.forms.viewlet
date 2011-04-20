# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages


name = 'dolmen.forms.viewlet'
version = '2.0a1dev'
readme = open(join('src', 'dolmen', 'forms', 'viewlet', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires=[
    'dolmen.forms.base',
    'dolmen.template',
    'dolmen.view',
    'dolmen.viewlet',
    'grokcore.component',
    'setuptools',
    'zope.component',
    'zope.interface',
    ]

tests_require = [
    'WebOb',
    'cromlech.io',
    'cromlech.webob',
    'dolmen.tales',
    'infrae.testbrowser',
    'zope.configuration',
    'zope.location',
    ]

setup(name=name,
      version=version,
      description="dolmen.forms forms in a viewlet",
      long_description=readme + "\n\n" + history,
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Dolmen Form Viewlet',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://pypi.python.org/pypi/dolmen.forms.viewlet',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['dolmen', 'dolmen.forms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      )
