# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    capital_currency_id = fields.Many2one(
        'res.currency',
        'Capital currency',
    )

    capital = fields.Float(
        'Capital currency',
    )

    revenue = fields.Float(
        'Revenue',
    )

    financial_data_year = fields.Integer(
        'Financial data year',
    )

    number_employees_min = fields.Integer(
        'Number employees',
    )
