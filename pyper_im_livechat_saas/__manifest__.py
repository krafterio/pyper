# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Im Livechat SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Im Livechatconfiguration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'im_livechat',
        'pyper_saas',
    ],
    'depends': [
        'im_livechat',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_templates.xml',
        'views/im_livechat_channel_templates.xml',
    ],
}
