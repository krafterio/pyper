# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    drop_contact_token_api = fields.Char(
        string="Drop Contact Token API",
        store=True,
        config_parameter='drop_contact_connector.token_api',
    )
