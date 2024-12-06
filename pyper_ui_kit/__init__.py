# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.addons.pyper.tools.view_validation import extend_relaxng
from . import models


extend_relaxng('base/rng/tree_view.rng', 'pyper_ui_kit/rng/tree_view.rng')


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Menu
    if icp.get_param('pyper_menu.provider.preferWebIcon', None) == 'True':
        icp.set_param('pyper_menu.provider.preferWebIcon', False)
