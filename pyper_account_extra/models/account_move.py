# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    display_bank_account_on_document = fields.Boolean(
        compute='_compute_display_bank_account_on_document',
    )

    hide_duplicate_reference = fields.Boolean(
        compute='_compute_hide_duplicate_reference',
    )

    hide_duplicate_customer_address = fields.Boolean(
        compute='_compute_hide_duplicate_customer_address',
    )

    main_partner_id = fields.Many2one(
        'res.partner',
        string='Main Partner',
        compute='_compute_main_partner_id',
        store=True,
        readonly=False,
    )

    @api.depends('partner_id')
    def _compute_main_partner_id(self):
        for move in self:
            partner = move.partner_id

            while partner and partner.parent_id:
                partner = partner.parent_id

            move.main_partner_id = partner

    @api.depends('partner_bank_id')
    def _compute_display_bank_account_on_document(self):
        for move in self:
            move.display_bank_account_on_document = (
                move.company_id.invoice_bank_account_in_report
                and move.partner_bank_id
            )

    @api.depends('ref', 'invoice_origin')
    def _compute_hide_duplicate_reference(self):
        for move in self:
            move.hide_duplicate_reference = (
                move.company_id.invoice_hide_duplicate_reference
                and move.ref
                and move.invoice_origin
                and move.ref == move.invoice_origin
            )

    @api.depends('partner_id')
    def _compute_hide_duplicate_customer_address(self):
        for move in self:
            partner = move.partner_id
            commercial = partner.commercial_partner_id
            if (
                not move.company_id.invoice_hide_duplicate_customer_address
                or commercial == partner
            ):
                move.hide_duplicate_customer_address = False
            else:
                move.hide_duplicate_customer_address = all(
                    partner[f] == commercial[f]
                    for f in ('street', 'street2', 'zip', 'city', 'country_id', 'state_id')
                )
