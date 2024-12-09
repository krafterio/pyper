# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_user = fields.Boolean(
        'Is user',
        compute="_compute_is_user",
        store=True,
    )

    employee_size = fields.Selection(
        [
            ('00', '1-10'),
            ('01', '11-50'),
            ('02', '51-200'),
            ('03', '201-500'),
            ('04', '501-1000'),
            ('05', '1001-5000'),
            ('06', '5001-10000'),
            ('07', '10000+'),
        ],
        'Employee size',
        placeholder='Select employee size',
    )

    @api.depends('user_ids')
    def _compute_is_user(self):
        for partner in self:
            partner.is_user = len(partner.user_ids) > 0

