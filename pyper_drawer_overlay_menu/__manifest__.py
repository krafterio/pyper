# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Drawer Overlay Menu',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Auto configure Drawer with Overlay Menu.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'pyper_drawer',
        'pyper_overlay_menu',
    ],
    'depends': [
        'base',
        'web',
        'pyper_drawer',
        'pyper_overlay_menu',
    ],
}
