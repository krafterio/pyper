# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_bank_account_in_report = fields.Boolean(
        'Bank account in sale order document?',
        config_parameter='pyper_sale_extra.bank_account_in_report',
    )
