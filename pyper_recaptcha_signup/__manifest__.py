# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'reCAPTCHA Signup',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Securing signup page with Google reCAPTCHA',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'auth_signup',
        'pyper_setup',
    ],
    'data': [
        # Views
        'views/res_config_views.xml',

        # Templates
        'views/webclient_templates.xml',
    ],
}
