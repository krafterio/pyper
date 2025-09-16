# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_bank_account_in_report = fields.Boolean(
        'Bank account in invoice document?',
    )
