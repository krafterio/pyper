# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from . import models


def post_init_hook(env):
    icp = env['ir.config_parameter'].sudo()
    if icp.get_param('disable_msg_post_recipients_subscribe', None) is None:
        icp.set_param('disable_msg_post_recipients_subscribe', 'True')
