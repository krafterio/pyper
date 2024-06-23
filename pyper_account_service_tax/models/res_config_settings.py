# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_service_tax_id = fields.Many2one(
        'account.tax',
        string='Default Sale Service Tax',
        related='company_id.account_sale_service_tax_id',
        readonly=False,
        check_company=True,
    )

    purchase_service_tax_id = fields.Many2one(
        'account.tax',
        string='Default Purchase Service Tax',
        related='company_id.account_purchase_service_tax_id',
        readonly=False,
        check_company=True,
    )
