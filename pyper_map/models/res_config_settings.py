# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import requests

from odoo import _, api, fields, models
from odoo.http import request


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pyper_map_provider = fields.Selection(
        [
            ('openstreetmap', 'OpenStreetMap'),
            ('mapbox', 'Mapbox'),
        ],
        config_parameter='pyper_map.provider',
        default='openstreetmap',
        required=True,
    )

    pyper_map_mapbox_token = fields.Char(
        'Mapbox Token',
        config_parameter='pyper_map.mapbox.token',
    )

    @api.onchange('pyper_map_mapbox_token')
    def _onchange_pyper_map_mapbox_token(self):
        if not self.pyper_map_mapbox_token:
            return

        token = self.env['ir.config_parameter'].get_param('pyper_map.mapbox.token')

        if self.pyper_map_mapbox_token == token:
            return

        url = 'https://api.mapbox.com/search/geocode/v6/forward?q=Hassegor%20France'
        headers = {
            'referer': request.httprequest.headers.environ.get('HTTP_REFERER'),
        }
        params = {
            'access_token': self.pyper_map_mapbox_token,
        }

        try:
            result = requests.head(url=url, headers=headers, params=params, timeout=5)
            error_code = result.status_code

            if not self.pyper_map_provider:
                self.pyper_map_provider = 'mapbox'
        except requests.exceptions.RequestException:
            error_code = 500

        if error_code == 200:
            return

        self.pyper_map_mapbox_token = False

        if error_code == 401:
            return {'warning': {'message': _('The token input is not valid')}}
        elif error_code == 403:
            return {'warning': {'message': _('This referer is not authorized')}}
        elif error_code == 500:
            return {'warning': {'message': _('The MapBox server is unreachable')}}
