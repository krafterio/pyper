# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Web Theme Icons',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Use app icons with Pyper Web Theme',
    'version': '1.1',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'pyper_fonts_phosphor',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'web',
        'pyper_menu',
        'pyper_fonts_phosphor',
        'pyper_web_theme',
    ],
}
