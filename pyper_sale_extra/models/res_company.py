# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_bank_account_in_report = fields.Boolean(
        'Bank account in sale order document?',
    )

    sale_signature_information_in_report = fields.Boolean(
        'Signature information in sale order document?',
    )

    sale_signature_information_text_in_report = fields.Text(
        'Text for signature information in sale order document',
        translate=True,
    )
