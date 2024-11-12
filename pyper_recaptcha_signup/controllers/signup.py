# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import json
import werkzeug
import requests

from odoo import http, _
from odoo.addons.web.controllers.utils import ensure_db
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request

class Signup(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, redirect=None, **kw):
        ensure_db()
        param = request.env['ir.config_parameter'].sudo().get_param

        if param('pyper_recaptcha_signup.enabled'):
            if request.httprequest.method == 'POST':
                secret_key = param('pyper_recaptcha_signup.private_key')
                captcha_result = self._check_grecaptcha(kw.get('g-recaptcha-response'), secret_key)

                if not captcha_result.get('success', False):
                    request.params['signup_success'] = False
                    values = request.params.copy()
                    values['error'] = self._get_grecaptcha_error_message(captcha_result.get('error-codes', None))
                    values['recaptcha_signup_enabled'] = True
                    values['providers'] = self._get_providers()

                    return request.render('auth_signup.signup', values)

            result = super(Signup, self).web_auth_signup(redirect=redirect, **kw)

            if request.httprequest.method == 'POST':
                if result.qcontext.get('error'):
                    request.params['signup_success'] = False
                    result.qcontext.update({
                        'error': _('Error to pass reCAPTCHA.')
                    })
                else:
                    request.params['signup_success'] = True
                    result.qcontext.update({
                        'recaptcha_signup_enabled': None,
                    })

            return result
        else:
            return super(Signup, self).web_auth_signup(redirect=redirect, **kw)

    @staticmethod
    def _get_providers():
        # Check if providers of auth_oauth addon are installed
        try:
            providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:
            providers = []

        for provider in providers:
            return_url = request.httprequest.url_root + 'auth_oauth/signin'
            state = Signup._get_state(provider)
            params = dict(
                response_type='token',
                client_id=provider['client_id'],
                redirect_uri=return_url,
                scope=provider['scope'],
                state=json.dumps(state),
            )

            provider['auth_link'] = '%s?%s' % (provider['auth_endpoint'], werkzeug.urls.url_encode(params))

        return providers

    @staticmethod
    def _get_state(provider):
        redirect = request.params.get('redirect') or 'web'

        if not redirect.startswith(('//', 'http://', 'https://')):
            redirect = '%s%s' % (request.httprequest.url_root, redirect[1:] if redirect[0] == '/' else redirect)

        state = dict(
            d=request.session.db,
            p=provider['id'],
            r=werkzeug.urls.url_quote_plus(redirect),
        )

        token = request.params.get('token')

        if token:
            state['t'] = token

        return state

    @staticmethod
    def _check_grecaptcha(response, secret_key):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {
            'secret': secret_key,
            'response': response,
            'remoteip': Signup._get_client_ip()
        }
        res = requests.get(url, params=params, verify=True)

        return res.json()

    @staticmethod
    def _get_client_ip():
        return request.env['ir.config_parameter'].sudo().get_param('web.base.url')

    @staticmethod
    def _get_grecaptcha_error_message(error_code):
        error_code_mapper = {
            'missing-input-secret': _('Secret parameter is missing, please inform the website administrator'),
            'invalid-input-secret': _('Secret parameter is invalid or malformed, please inform the website administrator'),
            'missing-input-response': _('reCAPTCHA is missing, please try again'),
            'invalid-input-response': _('reCAPTCHA is missing, invalid or malformed, please try again')
        }

        return error_code_mapper.get(
            error_code[0] if error_code else None,
            _('Please fill all entry and submit reCAPTCHA again')
        )
