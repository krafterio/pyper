# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.nav', None) is None:
        icp.set_param('pyper_drawer.drawer_props.nav', 'True')

    if icp.get_param('pyper_drawer.drawer_props.closeAction', None) is None:
        icp.set_param('pyper_drawer.drawer_props.closeAction', 'True')

    if icp.get_param('pyper_drawer.drawer_props.showCategorySectionMinified', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.showCategorySectionMinified', False)

    if icp.get_param('pyper_drawer.drawer_props.fixedTop', None) == 'True':
        icp.set_param('pyper_drawer.drawer_props.fixedTop', False)

    if icp.get_param('pyper_drawer.drawer_props.alwaysHeader', None) is None:
        icp.set_param('pyper_drawer.drawer_props.alwaysHeader', 'True')

    if icp.get_param('pyper_drawer.drawer_props.alwaysFooter', None) is None:
        icp.set_param('pyper_drawer.drawer_props.alwaysFooter', 'True')

    # Drawer Toggler
    if icp.get_param('pyper_drawer.drawer_toggler_props.useCaretIcon', None) == 'True':
        icp.set_param('pyper_drawer.drawer_toggler_props.useCaretIcon', False)

    if icp.get_param('pyper_drawer.drawer_toggler_props.autoHide', None) is None:
        icp.set_param('pyper_drawer.drawer_toggler_props.autoHide', 'True')
