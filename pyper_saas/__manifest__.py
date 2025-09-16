# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Configuration for SaaS',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'web',
    ],
    'post_load': 'post_load',
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
