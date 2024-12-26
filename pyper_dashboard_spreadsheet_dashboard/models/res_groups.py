# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = 'res.groups'

    active = fields.Boolean(
        'Active',
        default=True,
    )

    @api.model
    def get_groups_by_application(self):
        res = super().get_groups_by_application()
        filtered_res = []

        for item in res:
            if item[2]:
                filtered_groups = item[2].filtered(lambda g: g.active)

                if filtered_groups:
                    updated_item = item[:2] + (filtered_groups,) + item[3:]
                    filtered_res.append(updated_item)

        return filtered_res
