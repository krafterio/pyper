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

    has_field_access = fields.Boolean(
        string='Has access',
        compute='_compute_has_field_access',
    )

    @api.depends('access_ids')
    def _compute_has_field_access(self):
        for rec in self:
            rec.has_field_access = len(rec.access_ids.ids) > 0
