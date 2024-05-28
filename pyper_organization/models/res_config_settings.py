# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    organization_id = fields.Many2one(
        'organization',
        string='Organization',
        required=False,
        default=lambda self: self.env.organization,
    )
