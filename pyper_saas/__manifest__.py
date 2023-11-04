# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'web',
    ],
    'data': [
        'data/bot.xml',
        'data/rules.xml',

        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': {
            'pyper_saas/static/src/webclient/**/*.js',
        },
    },
}
