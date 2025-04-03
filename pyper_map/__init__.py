# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Default Map Provider
    icp.set_param('pyper_map.provider', 'openstreetmap')
