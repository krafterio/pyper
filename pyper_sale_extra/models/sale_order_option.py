# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

from odoo import fields, models, api


class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'

    currency_id = fields.Many2one('res.currency', compute='_compute_amount', store=True)

    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        compute='_compute_amount',
        check_company=True,
        store=True,
    )

    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True,
    )
    price_total = fields.Monetary(
        string="Total",
        compute='_compute_amount',
        store=True,
    )

    @api.depends('product_id', 'quantity', 'price_unit', 'discount')
    def _compute_amount(self):
        for option in self:
            if not option.product_id:
                continue
            values = option._get_values_to_add_to_order()
            new_sol = self.env['sale.order.line'].new(values)
            new_sol._compute_tax_id()
            new_sol._compute_amount()
            option.tax_id = new_sol.tax_id._origin
            option.currency_id = new_sol.currency_id
            option.price_subtotal= new_sol.price_subtotal
            option.price_total= new_sol.price_total
            # Avoid attaching the new line when called on template change
            new_sol.order_id = False

