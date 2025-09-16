# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'ReCAPTCHA Login',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Securing login page with Google reCAPTCHA',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'google_recaptcha',
    ],
    'data': [
        # Views
        'views/res_config_views.xml',

        # Templates
        'views/webclient_templates.xml',
    ],
}
