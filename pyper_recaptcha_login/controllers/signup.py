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

        if param('pyper_recaptcha_login.enabled'):
            max_error_attempt = param('pyper_recaptcha_login.max_error_attempt') or 0

            if max_error_attempt:
                max_error_attempt = int(max_error_attempt)

            max_error_attempt = max_error_attempt and max_error_attempt or 0
            failed_attempt = request.session.get('failed_attempt', 0)

            if request.httprequest.method == 'POST' and failed_attempt >= max_error_attempt:
                secret_key = param('pyper_recaptcha_login.private_key')
                captcha_result = self._check_grecaptcha(kw.get('g-recaptcha-response'), secret_key)

                if not captcha_result.get('success', False):
                    request.params['login_success'] = False
                    values = request.params.copy()
                    values['error'] = self._get_grecaptcha_error_message(captcha_result.get('error-codes', None))
                    values['recaptcha_login_enabled'] = True
                    values['providers'] = self._get_providers()

                    if not failed_attempt:
                        failed_attempt = 0

                    failed_attempt += 1
                    request.session['failed_attempt'] = failed_attempt

                    return request.render('auth_signup.signup', values)

            result = super(Signup, self).web_auth_signup(redirect=redirect, **kw)

            if request.httprequest.method == 'GET' and failed_attempt and (failed_attempt >= max_error_attempt):
                result.qcontext.update({
                    'recaptcha_login_enabled': True,
                    'error': _(
                        'Please, don\'t forgot to validate reCAPTCHA, maximum allowed error attempt is %(max)s.',
                        max=max_error_attempt,
                    ),
                })

            if request.httprequest.method == 'POST':
                if result.qcontext.get('error'):
                    if not failed_attempt:
                        failed_attempt = 0

                    failed_attempt += 1
                    request.session['failed_attempt'] = failed_attempt
                    request.params['login_success'] = False

                    if failed_attempt < max_error_attempt:
                        result.qcontext.update({
                            'error': _(
                                '%(error)s, login lockdown is enabled, you have left %(attempt)s attempt!',
                                error=result.qcontext.get('error'),
                                attempt=max_error_attempt - failed_attempt
                            )
                        })
                    else:
                        result.qcontext.update({
                            'error': _('Please don\'t forget to validate reCAPTCHA.')
                        })
                else:
                    failed_attempt = None
                    request.params['login_success'] = True
                    request.session['failed_attempt'] = failed_attempt
                    result.qcontext.update({
                        'recaptcha_login_enabled': None,
                    })

                if failed_attempt and failed_attempt >= max_error_attempt:
                    result.qcontext.update({
                        'recaptcha_login_enabled': True,
                        'error': _(
                            'Please, don\'t forgot to validate reCAPTCHA, maximum allowed error attempt is %(max)s.',
                            max=max_error_attempt,
                        ),
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
            state = Home._get_state(provider)
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
            'remoteip': Home._get_client_ip()
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
