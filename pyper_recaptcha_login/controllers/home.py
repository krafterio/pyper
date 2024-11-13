# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import json
import werkzeug
import requests

from odoo import http, _
from odoo.addons.web.controllers.utils import ensure_db
from odoo.addons.web.controllers.home import Home as BaseHome
from odoo.http import request
import logging

logger = logging.getLogger(__name__)


class Home(BaseHome):
    @http.route()
    def web_login(self, redirect=None, **kw):
        ensure_db()
        param = request.env['ir.config_parameter'].sudo().get_param

        if param('pyper_recaptcha_login.enabled'):
            if request.httprequest.method == 'POST':
                secret_key = param('pyper_recaptcha_login.private_key')
                min_score = param('pyper_recaptcha_login.min_score')
                captcha_result = self._check_grecaptcha(kw.get('g-recaptcha-response'), secret_key, min_score)

                if not captcha_result.get('success', False):
                    request.params['login_success'] = False
                    values = request.params.copy()
                    values['error'] = self._get_grecaptcha_error_message(captcha_result.get('error-codes', None))
                    values['recaptcha_login_enabled'] = True
                    values['providers'] = self._get_providers()

                    return request.render('web.login', values)

        return super(Home, self).web_login(redirect=redirect, **kw)

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
    def _check_grecaptcha(response, secret_key, min_score):
        url = 'https://www.recaptcha.net/recaptcha/api/siteverify'
        ip_addr = Home._get_client_ip()
        params = {
            'secret': secret_key,
            'response': response,
            'remoteip': ip_addr
        }
        res = {}
        try:
            res_raw = requests.get(url, params=params, verify=True)
            res = res_raw.json()
        except requests.exceptions.Timeout:
            logger.error("Trial captcha verification timeout for ip address %s", ip_addr)
            res.update({'success': False})
        except Exception:
            logger.error("Trial captcha verification bad request response")
            res.update({'success': False})

        res_success = res.get('success', False)
        if res_success:
            score = res.get('score', False)
            if score < float(min_score):
                logger.warning("Trial captcha verification for ip address %s failed with score %f.", ip_addr, score)
                res.update({'success': False, 'error-codes' : ['score-too-low'] })
        return res

    @staticmethod
    def _get_client_ip():
        return request.env['ir.config_parameter'].sudo().get_param('web.base.url')

    @staticmethod
    def _get_grecaptcha_error_message(error_code):
        error_code_mapper = {
            'missing-input-secret': _('Secret parameter is missing, please inform the website administrator'),
            'invalid-input-secret': _('Secret parameter is invalid or malformed, please inform the website administrator'),
            'missing-input-response': _('reCAPTCHA is missing, please try again'),
            'invalid-input-response': _('reCAPTCHA is missing, invalid or malformed, please try again'),
            'timeout-or-duplicate': _('reCAPTCHA request failed because of duplicate or timeout'),
            'bad-request': _('reCAPTCHA request failed due to a bad request'),
            'score-too-low': _('You did not reached the minimum score required for reCAPTCHA, are you a bot ?')
        }

        return error_code_mapper.get(
            error_code[0] if error_code else None,
            _('Action blocked by reCAPTCHA, please submit again or contact website administrator')
        )
