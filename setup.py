#! /usr/bin/env python3

from setuptools import setup


setup(
    name='tenant2landlord',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configlib',
        'emaillib',
        'flask',
        'functoolsplus',
        'his',
        'hwdb',
        'mdb',
        'notificationlib',
        'peewee',
        'peeweeplus',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    packages=['tenant2landlord'],
    license='GPLv3',
    description='HIS microservice to handle tenant-to-landlord messages.'
)
