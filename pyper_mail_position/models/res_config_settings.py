# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    chatter_position = fields.Selection(
        [
            ('auto', 'Responsive'),
            ('bottom', 'Bottom'),
            ('sided', 'Sided'),
        ],
        default='auto',
        required=True,
        config_parameter='pyper_mail_position.chatterPosition',
    )
