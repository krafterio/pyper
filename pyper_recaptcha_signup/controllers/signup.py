# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as BaseAuthSignupHome
from odoo.addons.web.controllers.utils import ensure_db
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
import logging

logger = logging.getLogger(__name__)


class AuthSignupHome(BaseAuthSignupHome):
    @http.route()
    def web_auth_signup(self, redirect=None, **kw):
        recaptcha_token = kw.pop('g-recaptcha-response', False)

        if recaptcha_token:
            try:
                ensure_db()
                param = request.env['ir.config_parameter'].sudo().get_param
                if param('pyper_recaptcha_signup.enabled') and request.httprequest.method == 'POST':
                    # Replace 'g-recaptcha-response' input by 'recaptcha_token_response' request params
                    request.params.update({'recaptcha_token_response': recaptcha_token})

                    if not request.env['ir.http']._verify_request_recaptcha_token('signup_form'):
                        raise UserError(_('Invalid recaptcha'))
            except (ValidationError, UserError) as e:
                request.params['signup_success'] = False
                values = request.params.copy()
                values.update({'error': str(e)})

                return request.render('auth_signup.signup', values)

        response = super().web_auth_signup(redirect=redirect, **kw)

        if not request.params.get('signup_success', False) and 'Content-Security-Policy' in request.params:
            response.headers.pop('Content-Security-Policy')

        return response
