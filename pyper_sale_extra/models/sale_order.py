# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from datetime import timedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    validity_days = fields.Integer(
        'Validity days',
        compute='_compute_validity_days',
        help='Number of days corresponding to the validity period',
    )

    @api.depends('validity_date', 'date_order')
    def _compute_validity_days(self):
        for sale in self:
            sale.validity_days = (sale.validity_date - sale.date_order.date()).days

    @api.onchange('validity_date')
    def _onchange_validity_date(self):
        self._compute_validity_days()

    @api.onchange('date_order')
    def _onchange_date_order(self):
        if self.validity_days and self.validity_days > 0:
            self.validity_date = self.date_order.date() + timedelta(days=self.validity_days)
