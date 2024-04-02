# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import controllers
from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Overlay Menu
    if icp.get_param('pyper_overlay_menu.overlay_menu_props.showRootApp', None) is None:
        icp.set_param('pyper_overlay_menu.overlay_menu_props.showRootApp', 'True')
