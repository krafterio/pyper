# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    display_bank_account_on_document = fields.Boolean(
        compute='_compute_display_bank_account_on_document',
    )

    @api.depends('partner_bank_id')
    def _compute_display_bank_account_on_document(self):
        display = self.env['ir.config_parameter'].sudo().get_param('pyper_account_extra.bank_account_in_report')

        for move in self:
            move.display_bank_account_on_document = display and move.partner_bank_id
