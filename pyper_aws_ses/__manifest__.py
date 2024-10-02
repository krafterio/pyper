# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'AWS SES',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'summary': 'Retrieve inbound emails from AWS SES stored in AWS S3',
    'description': """
Pyper AWS SES
=============

Allow to retrieve inbound emails from AWS SES (Simple Email Service) stored in AWS S3.
    """,
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'mail',
        'web',
    ],
    'data': [
        'views/fetchmail_server_views.xml',
    ],
}
