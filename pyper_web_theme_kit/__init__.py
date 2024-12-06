# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Menu
    if icp.get_param('pyper_menu.provider.preferWebIcon', None) == 'True':
        icp.set_param('pyper_menu.provider.preferWebIcon', False)
