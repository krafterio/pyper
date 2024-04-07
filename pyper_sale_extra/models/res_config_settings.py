# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_bank_account_in_report = fields.Boolean(
        'Bank account in sale order document?',
        related='company_id.sale_bank_account_in_report',
        readonly=False,
    )

    sale_signature_information_in_report = fields.Boolean(
        'Signature information in sale order document?',
        related='company_id.sale_signature_information_in_report',
        readonly=False,
    )

    sale_signature_information_text_in_report = fields.Text(
        'Text for signature information in sale order document',
        related='company_id.sale_signature_information_text_in_report',
        readonly=False,
        translate=True,
    )
