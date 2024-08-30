# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    google_ads_id = fields.Char(
        string="Google Ads ID",
        related='website_id.google_ads_id',
        readonly=False,
    )
