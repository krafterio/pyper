# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from datetime import timedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_bank_account_id = fields.Many2one(
        'res.partner.bank',
        'Main bank account',
        compute='_compute_main_bank_account_id',
        store=True,
        readonly=False,
        domain="[('partner_id', '=', id)]",
    )

    @api.depends('bank_ids')
    def _compute_main_bank_account_id(self):
        for partner in self:
            if partner.bank_ids:
                self.main_bank_account_id = partner.bank_ids[0]
            else:
                self.main_bank_account_id = False
