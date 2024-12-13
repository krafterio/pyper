# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    perplexity_token_api = fields.Char(
        string="Perplexity Token API",
        store=True,
        config_parameter='pyper_perplexity_connector.perplexity_token_api',
    )
