# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ReGroups(models.Model):
    _inherit = 'res.groups'

    field_access_ids = fields.One2many(
        'ir.model.fields.access',
        'group_id',
        'Field access rights',
    )
