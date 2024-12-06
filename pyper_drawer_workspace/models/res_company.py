# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    initials = fields.Char(
        'Initials',
        compute='_compute_initials',
    )

    @api.depends('name')
    def _compute_initials(self):
        for record in self:
            if record.name:
                record.initials = record.name[0:1].upper()
            else:
                record.initials = '?'
