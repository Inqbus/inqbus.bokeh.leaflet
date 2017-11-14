# -*- coding: utf-8 -*-
"""Installer for the inqbus.plone_bokeh package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='inqbus.bokeh.leaflet',
    version='0.1',
    description="Leaflet extension for bokeh",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python',
    author='volker',
    author_email='volker.jaenisch@inqbus.de',
    url='https://inqbus.de',
    license='Prorietary',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['inqbus', 'inqbus.bokeh'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'bokeh',
        'nodejs',
    ],
    extras_require={
        'test': [
        ],
    },
    entry_points="""
    [console_scripts]
    """,
)
