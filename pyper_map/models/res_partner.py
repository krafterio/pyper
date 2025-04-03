# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from collections import defaultdict

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    state_name = fields.Char(
        related='state_id.name',
        string='State Name',
    )

    @api.model
    def update_pyper_map_latitude_longitude(self, partners):
        partners_data = defaultdict(set)

        for partner in partners:
            if 'id' in partner and 'partner_latitude' in partner and 'partner_longitude' in partner:
                partners_data[(partner['partner_latitude'], partner['partner_longitude'])].add(partner['id'])

        for (lat, lng), ids in partners_data.items():
            self.browse(ids).sudo().write({
                'partner_latitude': lat,
                'partner_longitude': lng,
            })

        return {}

    @api.onchange('street', 'zip', 'city', 'state_id', 'country_id')
    def _delete_coordinates(self):
        self.partner_latitude = False
        self.partner_longitude = False
