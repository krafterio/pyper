# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_bank_account_in_report = fields.Boolean(
        'Bank account in invoice document?',
        related='company_id.invoice_bank_account_in_report',
        readonly=False,
    )
