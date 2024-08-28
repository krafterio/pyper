# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)

        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right
            field_names = list(res.keys())

            for field_name in field_names:
                if not check_right(self._name, field_name, 'read'):
                    del res[field_name]

        return res

    def export_data(self, fields_to_export):
        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right
            fields_to_export = [f for f in fields_to_export if check_right(self._name, f.replace('/', '.'), 'read')]

        return super().export_data(fields_to_export)

