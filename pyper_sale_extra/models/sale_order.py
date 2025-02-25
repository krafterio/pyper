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

    payment_method_id = fields.Many2one(
        'payment.provider',
        'Payment method',
        domain="[('payment_method_ids.active', '=', True)]",
        default=lambda self: self.env['payment.provider'].search(
            [('payment_method_ids.active', '=', True)],
            order='sequence ASC',
            limit=1,
        ),
        required=True,
    )

    display_bank_account_on_document = fields.Boolean(
        compute='_compute_display_bank_account_on_document',
    )

    display_signature_information_on_document = fields.Boolean(
        compute='_compute_display_signature_information_on_document',
    )

    main_partner_id = fields.Many2one(
        'res.partner',
        string='Main Customer',
        compute='_compute_main_partner_id',
        store=True,
        readonly=False,
    )

    display_details_optional_products = fields.Boolean(
        string='Display details of optional products on the document',
        default=True,
    )

    @api.depends('partner_id')
    def _compute_main_partner_id(self):
        for move in self:
            partner = move.partner_id

            while partner and partner.parent_id:
                partner = partner.parent_id

            move.main_partner_id = partner


    @api.depends('payment_method_id')
    def _compute_display_bank_account_on_document(self):
        for order in self:
            order.display_bank_account_on_document = (
                order.company_id.sale_bank_account_in_report
                and order.payment_method_id.payment_method_ids.filtered(lambda m: m.code == 'wire_transfer')
                and order.payment_method_id.journal_id.bank_account_id
            )

    @api.depends('company_id')
    def _compute_display_signature_information_on_document(self):
        for order in self:
            order.display_signature_information_on_document = (
                    not order.signature
                    and order.company_id.sale_signature_information_in_report
                    and order.company_id.sale_signature_information_text_in_report
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
