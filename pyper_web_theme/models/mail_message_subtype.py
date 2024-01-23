# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api


class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'

    value = fields.Char(
        'Value',
    )
