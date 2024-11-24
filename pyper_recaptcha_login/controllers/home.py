# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http, _
from odoo.addons.web.controllers.utils import ensure_db
from odoo.addons.web.controllers.home import Home as BaseHome
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
import logging

logger = logging.getLogger(__name__)


class Home(BaseHome):
    @http.route()
    def web_login(self, redirect=None, **kw):
        ensure_db()
        param = request.env['ir.config_parameter'].sudo().get_param

        if 'recaptcha_login' not in request.params:
            request.params.update({'recaptcha_login': param('pyper_recaptcha_login.enabled', False)})

        if not request.params.get('recaptcha_login'):
            return super().web_login(redirect=redirect, **kw)

        try:
            if request.httprequest.method == 'POST':
                # Replace 'g-recaptcha-response' input by 'recaptcha_token_response' request params
                request.params.update({'recaptcha_token_response': kw.pop('g-recaptcha-response', False)})

                if not request.env['ir.http']._verify_request_recaptcha_token('login_form'):
                    raise UserError(_('Invalid recaptcha'))
        except (ValidationError, UserError) as e:
            request.params['login_success'] = False
            values = request.params.copy()
            values.update({'error': str(e)})

            return request.render('web.login', values)

        response = super().web_login(redirect=redirect, **kw)

        if not request.params.get('login_success', False) and 'Content-Security-Policy' in response.headers:
            response.headers.pop('Content-Security-Policy')

        return response
