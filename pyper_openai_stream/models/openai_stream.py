# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import uuid

from odoo import fields, models


class OpenAiStream(models.TransientModel):
    _name = 'openai.stream'
    _description = 'Data Exchange for stream of Open AI'
    _transient_max_hours = 1.0

    identifier = fields.Char(
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
    )

    model = fields.Selection(
        [
            ('gpt-4o', 'GPT-4o'),
            ('chatgpt-4o-latest', 'GPT-4o Latest'),
            ('gpt-4o-mini', 'GPT-4o mini'),
            ('gpt-4-turbo', 'GPT-4 Turbo'),
            ('gpt-4', 'GPT-4'),
            ('gpt-3.5-turbo-0125', 'GPT-3.5 Turbo 0125'),
            ('gpt-3.5-turbo', 'PT-3.5 Turbo'),
        ],
        'Model',
        default='gpt-4o',
        required=True,
    )

    system_message = fields.Text(
        'System Message',
        required=False,
    )

    user_message = fields.Text(
        'User Message',
        required=True,
    )
