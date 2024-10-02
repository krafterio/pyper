# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pappers connector',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get company info from pappers',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'pyper_contact',
        'l10n_fr',
        'pyper_partner_scraper',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/partner_action.xml',

        # Views
        'views/conf_setting_views.xml',
        'views/res_partner_views.xml',

        # Wizard
        'wizard/pappers_name_form.xml',
        'wizard/pappers_form.xml',
        'wizard/menu.xml',
    ],
}
