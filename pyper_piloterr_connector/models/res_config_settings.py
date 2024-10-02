# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    piloterr_token_api = fields.Char(
        string="Piloterr Token API",
        store=True,
        config_parameter='piloterr_connector.piloterr_token_api',
    )
