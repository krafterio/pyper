# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def post_init_hook(env):
    env['ir.ui.menu'].sudo()._disable_spreadsheet_dashboard()
