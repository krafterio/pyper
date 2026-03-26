# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    phone_formatted = fields.Char(
        'Phone formatted',
        compute='_compute_phone_formatted',
        compute_sudo=True,
        store=True,
    )

    @api.depends('phone')
    def _compute_phone_formatted(self):
        for record in self:
            record.phone_formatted = record._phone_format(fname='phone') if record.phone else False
