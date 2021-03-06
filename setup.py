# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
    'pylint',
    'factory-boy',
    'pylint-plugin-utils'
]


docs_extras = [
]

tests_require = [
    "django>=1.7"
    "srcgen"
]

testing_extras = tests_require + [
]

setup(name='pylint-factory-boy-django',
      version='0.1',
      description='a pylint plugin for factory boy in django environement',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='',
      author="",
      author_email="",
      url="",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      test_suite="pylint_factory_boy_django.tests",
      entry_points="""
""")

