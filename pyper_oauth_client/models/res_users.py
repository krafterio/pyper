# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models, fields, _
from ast import literal_eval
from odoo.tools.misc import ustr
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.exceptions import AccessDenied, UserError
import json


class ResUsers(models.Model):
    _inherit = 'res.users'

    refresh_token = fields.Char('Refresh Token', copy=False)

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """ retrieve and sign in the user corresponding to provider and validated access token
            :param provider: oauth provider id (int)
            :param validation: result of validation of access token (dict)
            :param params: oauth parameters (dict)
            :return: user login (str)
            :raise: AccessDenied if signin failed

            This method can be overridden to add alternative signin methods.
        """
        oauth_uid = validation['user_id']
        try:
            oauth_user = self.search([("oauth_uid", "=", oauth_uid), ('oauth_provider_id', '=', provider)])
            if not oauth_user:
                raise AccessDenied()
            assert len(oauth_user) == 1
            oauth_user.write({'oauth_access_token': params['access_token']})
            oauth_user.write({'refresh_token': params.get('refresh_token')})
            return oauth_user.login
        except AccessDenied as access_denied_exception:
            if self.env.context.get('no_user_creation'):
                return None
            oauth_user = self.search([('email', '=', validation.get('email'))])
            if oauth_user:
                oauth_user.write({'oauth_access_token': params['access_token']})
                oauth_user.write({'refresh_token': params.get('refresh_token')})
                return oauth_user.login

            state = json.loads(params['state'])
            token = state.get('t')
            values = self._generate_signup_values(provider, validation, params)
            if validation.get('image_1920'):
                values['image_1920'] = validation.get('image_1920')
            if params.get('refresh_token'):
                values['refresh_token'] = params.get('refresh_token')
            provider_id = self.env['auth.oauth.provider'].browse(provider)
            values['user_type'] = provider_id.type_user_create
            try:
                login, _ = self.signup(values, token)
                return login
            except (SignupError, UserError):
                raise access_denied_exception

    @api.model
    def _create_user_from_template(self, values):
        user_type = values.get('user_type', 'portal')

        if user_type == 'internal':
            template_user_id = literal_eval(
                self.env['ir.config_parameter'].sudo().get_param('oauth_client.template_internal_user_id', 'False')
            )
            values.pop('user_type')
        else:
            template_user_id = literal_eval(
                self.env['ir.config_parameter'].sudo().get_param('base.template_portal_user_id', 'False')
            )

        template_user = self.browse(template_user_id)

        if not template_user.exists():
            raise ValueError(_('Signup: invalid template user'))

        if not values.get('login'):
            raise ValueError(_('Signup: no login given for new user'))
        if not values.get('partner_id') and not values.get('name'):
            raise ValueError(_('Signup: no name or partner given for new user'))

        values['active'] = True
        try:
            with self.env.cr.savepoint():
                return template_user.with_context(no_reset_password=True).copy(values)
        except Exception as e:
            raise SignupError(ustr(e))

    def revoke_oauth_access_token(self):
        self.write({'oauth_access_token': False, 'refresh_token': False})
        
        return True
