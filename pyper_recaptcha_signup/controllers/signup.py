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
        ensure_db()
        param = request.env['ir.config_parameter'].sudo().get_param

        if 'recaptcha_signup' not in request.params:
            request.params.update({
                'recaptcha_signup': param('pyper_recaptcha_signup.enabled', False),
                'recaptcha_login': False, # Disable recaptcha on login in same request if it enabled
            })

        if not request.params.get('recaptcha_signup'):
            return super().web_auth_signup(redirect=redirect, **kw)

        try:
            if request.httprequest.method == 'POST':
                # Replace 'g-recaptcha-response' input by 'recaptcha_token_response' request params
                request.params.update({'recaptcha_token_response': kw.pop('g-recaptcha-response', False)})

                if not request.env['ir.http']._verify_request_recaptcha_token('signup_form'):
                    raise UserError(_('Invalid recaptcha'))
        except (ValidationError, UserError) as e:
            request.params['signup_success'] = False
            values = request.params.copy()
            values.update({'error': str(e)})

            return request.render('auth_signup.signup', values)

        response = super().web_auth_signup(redirect=redirect, **kw)

        if not request.params.get('signup_success', False) and 'Content-Security-Policy' in response.headers:
            response.headers.pop('Content-Security-Policy')

        return response
