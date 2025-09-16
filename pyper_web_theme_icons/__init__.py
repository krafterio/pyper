# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from . import models


def post_init_hook(env):
    env['ir.ui.menu'].sudo()._update_root_icons()
