# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Mail AI',
    'category': 'Productivity/Discuss',
    'license': 'Other proprietary',
    'description': 'Sync all messages from IMAP account',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'mail',
        'pyper_openai_connector',
        'pyper_openai_stream',
    ],
    'data': [
        # Data
        'data/mail_template_ai_config_data.xml',
        'data/mail_template_ai_model_data.xml',

        # Security
        'security/ir.model.access.csv',

        # Views
        'views/mail_template_ai_config_views.xml',
        'views/mail_template_ai_model_views.xml',
        'views/mail_template_views.xml',

        # Wizard
        'wizard/mail_compose_message_views.xml',

        # Menu
        'views/menu.xml',
    ],
}
