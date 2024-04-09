# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Drawer
    if icp.get_param('pyper_drawer.drawer_props.showRootApp', None) is None:
        icp.set_param('pyper_drawer.drawer_props.showRootApp', 'True')

    if icp.get_param('pyper_drawer.drawer_props.fixedTop', None) is None:
        icp.set_param('pyper_drawer.drawer_props.fixedTop', 'True')

    if icp.get_param('pyper_drawer.drawer_props.minifiable', None) is None:
        icp.set_param('pyper_drawer.drawer_props.minifiable', 'True')

    if icp.get_param('pyper_drawer.drawer_props.popoverMinified', None) is None:
        icp.set_param('pyper_drawer.drawer_props.popoverMinified', 'True')

    if icp.get_param('pyper_drawer.drawer_props.closeOnClick', None) is None:
        icp.set_param('pyper_drawer.drawer_props.closeOnClick', 'True')

    # Drawer Toggler
    if icp.get_param('pyper_drawer.drawer_toggler_props.useCaretIcon', None) is None:
        icp.set_param('pyper_drawer.drawer_toggler_props.useCaretIcon', 'True')
