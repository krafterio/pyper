# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    kaspr_token_api = fields.Char(
        string="Kaspr Token API",
        store=True,
        config_parameter='kaspr_connector.kaspr_token_api',
    )
