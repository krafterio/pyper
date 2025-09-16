# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_under_maintenance = fields.Boolean(
        related='website_id.is_under_maintenance',
        readonly=False,
    )

    under_maintenance_page = fields.Many2one(
        related='website_id.under_maintenance_page',
        readonly=False,
    )
