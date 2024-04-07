# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_bank_account_in_report = fields.Boolean(
        'Bank account in invoice document?',
        config_parameter='pyper_account_extra.bank_account_in_report',
    )
