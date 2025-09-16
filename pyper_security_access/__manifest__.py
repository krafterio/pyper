# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Security Access',
    'category': 'Technical',
    'license': 'LGPL-3',
    'description': 'Allow to add security access management on all models.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/ir_model_fields_access_views.xml',
        'views/ir_model_fields_views.xml',
        'views/ir_model_views.xml',
        'views/res_group_views.xml',
    ],
}
