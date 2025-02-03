# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
import requests
import logging

_logger = logging.getLogger(__name__)


class HomeOauth(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])

        if not user.oauth_uid or not user.oauth_access_token or not user.oauth_provider_id:
            return super().web_client(s_action, **kw)
        
        try:
            response = requests.post(
                f"{user.oauth_provider_id.validation_endpoint}?access_token={user.oauth_access_token}",
                timeout=5
            )
            response.raise_for_status()
            
        except requests.RequestException as e:
            _logger.error(f"OAuth token validation failed: {e}")

            if response.status_code == 401 and response.json().get('error') == 'expired_token':
                if not user.refresh_token:
                    _logger.warning("No refresh token found, forcing logout")
                    raise http.SessionExpiredException("No refresh token found")

                if not user.oauth_provider_id.token_endpoint:
                    _logger.warning("Missing token endpoint, cannot refresh token")
                    raise http.SessionExpiredException("Missing token endpoint, can't get a new token")

                try:
                    refresh_response = requests.post(
                        user.oauth_provider_id.token_endpoint,
                        json={
                            'grant_type': 'refresh_token',
                            'refresh_token': user.refresh_token,
                            'client_id': user.oauth_provider_id.client_id,
                            'client_secret': user.oauth_provider_id.client_secret
                        },
                        timeout=5
                    )
                    refresh_response.raise_for_status()

                    new_token_data = refresh_response.json()
                    user.write({'oauth_access_token': new_token_data.get('access_token')})

                    _logger.info("OAuth access token refreshed successfully")
                    return super().web_client(s_action, **kw)

                except requests.RequestException as e:
                    _logger.error(f"Failed to refresh token: {e}")
                    raise http.SessionExpiredException("Cannot refresh token")

            else:
                _logger.warning("Invalid or missing OAuth token, forcing logout")
                raise http.SessionExpiredException("Invalid or missing token")

        return super().web_client(s_action, **kw)
