# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    date_range_fy_id = fields.Many2one(
        'account.fiscal.year',
        related='move_id.date_range_fy_id',
        store=True,
    )

    _depends = {
        'account.move': [
            'date_range_fy_id',
        ],
    }

    @api.model
    def _select(self):
        return super()._select() + ''',
                move.date_range_fy_id
        '''

    @api.model
    def _from(self):
        return super()._from() + '''
                LEFT JOIN account_fiscal_year fiscal_year ON fiscal_year.id = move.date_range_fy_id
        '''
