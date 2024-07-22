# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    pappers_token_api = fields.Char(
        string="Pappers Token API",
        store=True,
        config_parameter='pappers_connector.pappers_token_api',
    )
