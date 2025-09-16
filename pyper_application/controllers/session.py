# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import logging
import uuid

import odoo
import odoo.modules.registry
from odoo.exceptions import AccessError
from odoo.http import Controller, db_filter, db_list, request, route

_logger = logging.getLogger(__name__)


def get_db():
    db = request.db

    if db:
        request.env.cr.rollback()
    else:
        dbs = db_list()
        db = dbs[0] if dbs else None

    if not db_filter([db]):
        raise AccessError('Database not found.')

    return db

class Session(Controller):
    @route('/app-ext/session/authenticate', type='json', auth='none', cors='*', save_session=False)
    def authenticate(self, login, password):
        db = get_db()
        uid = request.session.authenticate(db, login, password)

        if uid != request.session.uid:
            return {'uid': None}

        request.session.db = db
        registry = odoo.modules.registry.Registry(db)

        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, request.session.uid, request.session.context)
            icp = request.env['ir.config_parameter'].sudo()
            name = icp.get_param('pyper_application.app_name', self._get_default_token_name())
            token_name = name + ' (' + uuid.uuid4().hex + ')'

            info = {
                'db': db,
                'uid': uid,
                'username': env.user.login,
                'fullname': env.user.name,
                'avatar_128': env.user.avatar_128 or False,
                'token': env['res.users.apikeys']._generate(None, token_name),
                'token_name': token_name,
                'lang': env.context.get('lang', 'en'),
                'tz': env.context.get('tz', 'UTC'),
            }

            request.session.logout()

            return info

    @route('/app-ext/session/logout', type='json', auth='none', cors='*', save_session=False)
    def logout(self, token_name):
        authorization = request.httprequest.headers.get('Authorization')
        if authorization.startswith('Bearer '):
            authorization = authorization[7:]

        db = get_db()
        uid = request.env['res.users.apikeys']._check_credentials(scope='rpc', key=authorization)

        if not uid:
            raise AccessError('Invalid credentials.')

        request.session.db = db
        registry = odoo.modules.registry.Registry(db)

        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, uid, request.env.context)
            env['res.users.apikeys'].search([('name', '=', token_name)]).sudo().unlink()

    def _get_default_token_name(self):
        return 'Pyper Application'
