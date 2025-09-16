# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from openai import OpenAI, APIError
from werkzeug.exceptions import BadRequest, NotFound

from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import request


class Stream(http.Controller):
    @http.route('/openai/stream', type='json', auth='user', methods=['POST'])
    def initialize_stream(self, **kwargs):
        openai_token = request.env['ir.config_parameter'].sudo().get_param('pyper_openai_connector.openai_token_api')

        if not openai_token:
            raise UserError(_('The API token for Open AI must be configured before to communicate with the service'))

        user_message = kwargs.get('user_message', False)
        model = kwargs.get('model', False)

        if not user_message:
            raise BadRequest(_('User message is required'))

        vals = {
            'user_message': user_message,
            'system_message': kwargs.get('system_message', False),
        }

        if model:
            vals.update({'model': model})

        stream = request.env['openai.stream'].sudo().create(vals)

        return {
            'identifier': stream.identifier,
        }

    @http.route('/openai/stream/<identifier>', type='http', auth='user', methods=['GET'])
    def my_custom_event_source(self, identifier):
        stream = request.env['openai.stream'].sudo().search([('identifier', '=', identifier)], limit=1)

        if not stream:
            return NotFound(_('Stream not found'))

        api_key = request.env['ir.config_parameter'].sudo().get_param('pyper_openai_connector.openai_token_api')

        model = stream.model
        system_message = stream.system_message
        user_message = stream.user_message
        stream.unlink()

        return request.make_response(
            self.event_stream(api_key, model, system_message, user_message),
            headers=[
                ('Content-Type', 'text/event-stream'),
                ('Cache-Control', 'no-cache'),
                ('Connection', 'keep-alive'),
            ]
        )

    @staticmethod
    def event_stream(api_key, model, system_message, user_message):
        try:
            client = OpenAI(api_key=api_key)
            messages = []

            if system_message:
                messages.append({
                    'role': 'system',
                    'content': system_message,
                })

            messages.append({
                'role': 'user',
                'content': user_message,
            })

            response = client.chat.completions.create(
                model=model,
                stream=True,
                messages=messages,
            )

            for line in response:
                text = line.choices[0].delta.content

                if text:
                    yield f"data: {text}\n\n"

            yield "event: end\ndata: end\n\n"
        except Exception as e:
            if isinstance(e, APIError):
                message = e.body.get('message', str(e)) if isinstance(e.body, dict) else str(e)
            else:
                message = str(e)

            yield f"event: error\ndata: {message}\n\n"
            yield "event: end\ndata: end\n\n"
