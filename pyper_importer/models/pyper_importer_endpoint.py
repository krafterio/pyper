# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class PyperImporterEndpoint(models.Model):
    _name = 'pyper.importer.endpoint'
    _description = 'Importer Endpoint'
    _rec_name = 'endpoint_base_url'

    active = fields.Boolean(
        'Active',
        default=True,
    )

    endpoint_base_url = fields.Char(
        'Endpoint Base URL',
        required=True,
    )

    disable_ssl_verification = fields.Boolean(
        'Disable SSL verification',
    )

    default_batch_size = fields.Char(
        'Default batch size',
    )

    auth_type = fields.Selection(
        selection=[
            ('none', 'None'),
            ('basic', 'Basic'),
        ],
        ondelete={'basic': 'set default'},
        default='none',
        required=True,
    )

    auth_username = fields.Char(
        'Auth Username',
    )

    auth_password = fields.Char(
        'Auth Password',
    )
