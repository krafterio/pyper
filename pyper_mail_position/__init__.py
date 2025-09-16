# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()

    # Chatter Position
    if icp.get_param('pyper_mail_position.chatterPosition', None) is None:
        icp.set_param('pyper_mail_position.chatterPosition', 'auto')
