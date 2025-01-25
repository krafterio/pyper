# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Kaspr connector',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get contact info from linkedin from Kaspr',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'pyper_contact',
        'pyper_linkedin_partner',
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
        'wizard/kaspr_form.xml',
        'wizard/kaspr_form_views.xml',
    ],
}
