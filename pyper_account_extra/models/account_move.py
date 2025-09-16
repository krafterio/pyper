# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    display_bank_account_on_document = fields.Boolean(
        compute='_compute_display_bank_account_on_document',
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
