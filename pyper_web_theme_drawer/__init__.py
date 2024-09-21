# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.nav', None) is None:
        icp.set_param('pyper_drawer.drawer_props.nav', 'True')

    if icp.get_param('pyper_drawer.drawer_props.showCategorySectionMinified', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.showCategorySectionMinified', False)

    if icp.get_param('pyper_drawer.drawer_props.alwaysFooter', None) is None:
        icp.set_param('pyper_drawer.drawer_props.alwaysFooter', 'True')

    if icp.get_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', None) is None:
        icp.set_param('pyper_drawer.drawer_props.hideNavbarAppsMenu', 'True')

    # Drawer Toggler
    if icp.get_param('pyper_drawer.drawer_toggler_props.useCaretIcon', None) == 'True':
        icp.set_param('pyper_drawer.drawer_toggler_props.useCaretIcon', False)
