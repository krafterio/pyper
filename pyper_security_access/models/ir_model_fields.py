# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    access_ids = fields.One2many(
        'ir.model.fields.access',
        'field_id',
        'Access rights',
    )

    has_access = fields.Boolean(
        string='Has access',
        compute='_compute_has_access',
    )

    @api.depends('access_ids')
    def _compute_has_access(self):
        for rec in self:
            rec.has_access = len(rec.access_ids.ids) > 0
