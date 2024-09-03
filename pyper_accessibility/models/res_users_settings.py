# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    font_size = fields.Selection(
        [
            ('100', '100%'),
            ('125', '125%'),
            ('150', '150%'),
            ('175', '175%'),
            ('200', '200%'),
        ],
        'Font size',
        default='100',
        required=True,
    )
