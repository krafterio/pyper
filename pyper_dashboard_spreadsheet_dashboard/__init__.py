# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from . import models


def post_init_hook(env):
    env['res.config.settings'].sudo()._disable_spreadsheet_dashboard()
