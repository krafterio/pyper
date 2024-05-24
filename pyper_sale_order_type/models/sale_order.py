# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    type = fields.Selection(
        [
            ('classic', 'Classic'),
        ],
        string='Type',
        required=True,
        default='classic',
    )

