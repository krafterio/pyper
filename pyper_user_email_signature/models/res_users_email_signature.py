# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from markupsafe import Markup

from odoo import api, fields, models


class ResUsersEmails(models.Model):
    _name = 'res.users.email_signature'
    _description = 'User Emails'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        ondelete='cascade',
    )

    name = fields.Char(
        string='Name',
        required=True,
    )

    email = fields.Char(
        string='Email',
        required=True,
    )

    signature = fields.Html(
        string='Email Signature',
        compute='_compute_signature',
        readonly=False,
        store=True,
    )

    @api.depends('user_id', 'user_id.name')
    def _compute_signature(self):
        for email in self:
            email.signature = Markup('<p>--<br />%s</p>') % email.user_id.name
