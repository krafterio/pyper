# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_sale_service_tax_id = fields.Many2one(
        'account.tax',
        string='Default Sale Service Tax',
        check_company=True,
    )

    account_purchase_service_tax_id = fields.Many2one(
        'account.tax',
        string='Default Purchase Service Tax',
        check_company=True,
    )
