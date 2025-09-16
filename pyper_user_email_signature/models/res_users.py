# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    additional_email_signatures = fields.One2many(
        'res.users.email_signature',
        'user_id',
        string='Additional email signatures',
    )
