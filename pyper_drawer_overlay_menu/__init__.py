# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', False)
