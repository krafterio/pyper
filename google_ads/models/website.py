# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class Website(models.Model):
    _inherit = 'website'

    google_ads_id = fields.Char(
        string="Google Ads ID",
    )
