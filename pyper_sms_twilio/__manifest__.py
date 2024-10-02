# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'SMS Twilio',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Use Twilio to send SMS messages.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'iap',
        'pyper_iap',
        'sms',
    ],
    'data': [
        # Views
        'views/iap_account_views.xml',
    ],
}
