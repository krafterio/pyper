# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http, fields
from odoo.http import request
from datetime import timedelta
import secrets
import json
import werkzeug


class OAuth2Controller(http.Controller):
    
    @http.route('/oauth2/token', type='http', auth='none', csrf=False, methods=['POST'])
    
    def token(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            grant_type = data.get('grant_type')

            if grant_type not in ['authorization_code', 'refresh_token']:
                return http.Response(json.dumps({'error': 'unsupported_grant_type'}), status=400, mimetype='application/json')

            client_secret = data.get('client_secret')
            client_id = data.get('client_id')

            if not client_id or not client_secret:
                return http.Response(json.dumps({'error': 'missing_client_credentials'}), status=400, mimetype='application/json')

            client = request.env['oauth.client'].sudo().search([
                ('client_id', '=', client_id),
                ('client_secret', '=', client_secret)
            ], limit=1)

            if not client:
                return http.Response(json.dumps({'error': 'invalid_client'}), status=401, mimetype='application/json')

            if grant_type == 'authorization_code':
                authorization = data.get('authorization')
                user_id = data.get('user_id')

                if not authorization or not user_id:
                    return http.Response(
                        json.dumps({'error': 'missing_data'}),
                        status=400,
                        mimetype='application/json'
                    )

                authorization_id = request.env['oauth.authorization'].sudo().search([
                    ('token', '=', authorization)
                ], limit=1)

                if not authorization_id:
                    return http.Response(
                        json.dumps({'error': 'invalid_authorization'}),
                        status=401,
                        mimetype='application/json'
                    )

                authorization_id.unlink()

                refresh_token = request.env['oauth.refresh_token'].sudo().create({
                    'token': secrets.token_urlsafe(64),
                    'expires_at': fields.Datetime.now() + timedelta(days=365)
                })
                access_token = secrets.token_urlsafe(64)

                token = request.env['oauth.token'].sudo().create({
                    'client_id': client.id,
                    'scope': data.get('scope'),
                    'user_id': user_id,
                    'expires_at': fields.Datetime.now() + timedelta(minutes=60),
                    'token': access_token,
                    'refresh_token': refresh_token.id
                })
                if not token:
                    return http.Response(
                        json.dumps({'error': 'token_creation_failed'}),
                        status=500,
                        mimetype='application/json'
                    )

                return http.Response(
                    json.dumps({'access_token': access_token, 'refresh_token': refresh_token.token}),
                    status=200,
                    mimetype='application/json'
                )

            elif grant_type == 'refresh_token':
                refresh_token = data.get('refresh_token')

                if not refresh_token:
                    return http.Response(
                        json.dumps({'error': 'missing_refresh_token'}),
                        status=400,
                        mimetype='application/json'
                    )

                refresh_token_id = request.env['oauth.refresh_token'].sudo().search([
                    ('token', '=', refresh_token)
                ], limit=1)

                if not refresh_token_id or refresh_token_id.is_expired:
                    return http.Response(
                        json.dumps({'error': 'invalid_refresh_token'}),
                        status=401,
                        mimetype='application/json'
                    )

                token = request.env['oauth.token'].sudo().search([
                    ('refresh_token.token', '=', refresh_token),
                    ('client_id.client_id', '=', client_id),
                    ('client_id.client_secret', '=', client_secret)
                ], limit=1)

                if not token:
                    return http.Response(
                        json.dumps({'error': 'invalid_refresh_token'}),
                        status=401,
                        mimetype='application/json'
                    )

                token.write({
                    'token': secrets.token_urlsafe(64),
                    'expires_at': fields.Datetime.now() + timedelta(minutes=60)
                })

                return http.Response(
                    json.dumps({'access_token': token.token}),
                    status=200,
                    mimetype='application/json'
                )
        
        except Exception as e:
            return http.Response(json.dumps({'error': 'server_error', 'message': str(e)}), status=500, mimetype='application/json')

    #Token authorization endpoint is used to get user consent
    @http.route('/oauth2/auth', type='http', auth='user', csrf=False)
    def auth(self, **kwargs):
        client_id = kwargs.get('client_id')
        state = kwargs.get('state')
        scope = kwargs.get('scope')
        user_already_logged_in = True
        scope_changed = False

        if not client_id or not state or not scope:
            return http.Response(json.dumps({'error': 'missing_data'}), status=400, mimetype='application/json')
        
        client = request.env['oauth.client'].sudo().search([
            ('client_id', '=', client_id)
        ], limit=1)

        if not client:
            return http.Response(json.dumps({'error': 'invalid_client'}), status=401, mimetype='application/json')

        redirect_uri = client.redirect_uris.split(',')[0]
        if not redirect_uri.startswith('http'):
            return http.Response(json.dumps({'error': 'invalid_redirect_uri'}), status=400, mimetype='application/json')

        if not client.scopes:
            client.write({'scopes': scope})
        
        if set(client.scopes.split(',')) != set(scope.split(',')):
            scope_changed = True
            client.write({'scopes': scope})

        redirect_uri = f'{redirect_uri}/oauth2/callback'

        scopes = request.env['oauth.scope'].sudo().search([
            ('name', 'in', scope.split(','))
        ])
        if not 'userinfo' in scope:
            return http.Response(json.dumps({'error': 'insufficient_scope'}), status=403, mimetype='application/json')
        
        if request.env.user.id not in client.user_ids.ids:
            user_already_logged_in = False

        accessed = [d for s in scopes for d in s.description.split(',')]
        accessed = list(set(accessed))

        if client.skip_authorization or not scope_changed and user_already_logged_in:
            return request.redirect('/oauth2/authorize?response_type=allow&client_id={}&state={}&redirect_uri={}&scope={}'.format(
                client_id, state, redirect_uri, scopes
            ), local=False)

        return request.render('custom_oauth_provider.auth', {
            'client': client,
            'state': state,
            'redirect_uri': redirect_uri,
            'scopes': accessed,
            'user': request.env.user,
        })
    
    @http.route('/oauth2/authorize', type='http', auth='user', csrf=False)
    def authorize(self, **kwargs):
        state = kwargs.get('state')
        response_type = kwargs.get('response_type')
        client_id = kwargs.get('client_id')
        redirect_uri = kwargs.get('redirect_uri')
        if not response_type or not client_id or not redirect_uri:
            return 'Invalid request'

        client = request.env['oauth.client'].sudo().search([
            ('client_id', '=', client_id)
        ], limit=1)

        if not client:
            return http.Response(json.dumps({'error': 'invalid_client'}), status=401, mimetype='application/json')

        if response_type == 'allow':
            if request.env.user.id not in client.user_ids.ids:
                client.write({'user_ids': [(4, request.env.user.id)]})
            auth_code = request.env['oauth.authorization'].sudo().create({
                'token': secrets.token_urlsafe(64)
            })
            return request.redirect(f'{redirect_uri}?authorization={auth_code.token}&state={state}&client_id={client_id}&redirect_uri={redirect_uri}&user_id={request.env.user.id}', local=False)
        else:
            return request.redirect(f'{redirect_uri}web/login', local=False)

    @http.route('/oauth2/userinfo', type='http', auth='none', csrf=False)
    def userinfo(self, **kwargs):
        access_token = kwargs.get('access_token')
        if not access_token:
            return http.Response(
                json.dumps({'error': 'missing_token'}),
                status=400,
                mimetype='application/json'
            )
        token = request.env['oauth.token'].sudo().search([
            ('token', '=', access_token)
        ], limit=1)
        if not token:
            return http.Response(
                json.dumps({'error': 'invalid_token'}),
                status=401,
                mimetype='application/json'
            )
        if token.is_expired:
            return http.Response(
                json.dumps({'error': 'expired_token'}),
                status=401,
                mimetype='application/json'
            )
        scope = token.scope.split(',')
        if 'userinfo' not in scope:
            return http.Response(
                json.dumps({'error': 'insufficient_scope'}),
                status=403,
                mimetype='application/json'
            )
        return http.Response(
            json.dumps({
                'user_id': token.user_id.id,
                'email': token.user_id.email,
                'name': token.user_id.name,
                'image_1920': token.user_id.image_1920.decode() if token.user_id.image_1920 else None
            }),
            status=200,
            mimetype='application/json'
        )
