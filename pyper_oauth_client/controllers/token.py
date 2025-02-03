# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
import requests


class TokenController(http.Controller):

    @http.route('/oauth2/callback', type='http', auth='public', methods=['GET'], csrf=False)
    def get_token(self, **kwargs):
        redirect_uri = kwargs.get('redirect_uri')
        auth_code = kwargs.get('authorization')
        client_id = kwargs.get('client_id')
        user_id = kwargs.get('user_id')
        provider_id = request.env['auth.oauth.provider'].sudo().search([('client_id', '=', client_id)])
        state = kwargs.get('state')

        if not provider_id:
            return http.Response("Invalid client_id", status=400)

        if not redirect_uri or not auth_code:
            return http.Response("Missing parameters", status=400)
        data = {
            'grant_type': 'authorization_code',
            'authorization': auth_code,
            'redirect_uri': redirect_uri,
            'scope': provider_id.scope,
            'client_id': client_id,
            'client_secret': provider_id.client_secret,
            'user_id': user_id
        }
        
        response = requests.post(
            provider_id.token_endpoint,
            json=data
        )
        if response.status_code != 200:
            return http.Response("Invalid authorization code", status=400)
        response_data = response.json()
        token_data = {
            'access_token': response_data.get('access_token'),
            'refresh_token': response_data.get('refresh_token')
        }

        return request.redirect("auth_oauth/signin?access_token=%s&state=%s&refresh_token=%s" % (token_data['access_token'], state, token_data['refresh_token']))
