# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models
from odoo.addons.base_import.models.base_import import FIELDS_RECURSION_LIMIT


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    @api.model
    def get_fields_tree(self, model, depth=FIELDS_RECURSION_LIMIT):
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        fields = super().get_fields_tree(model, depth)

        return [f for f in fields if check_right(model, f.get('name'), 'write')]
