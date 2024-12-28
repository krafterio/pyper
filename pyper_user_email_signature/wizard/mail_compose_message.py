# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class MailComposerMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    user_email_signature = fields.Many2one(
        'res.users.email_signature',
        'Email signature',
        help='Use another email signature to send an email',
    )

    has_user_email_signature = fields.Boolean(
        'Has user email signature?',
        store=False,
        default=lambda self: self.env['res.users.email_signature'].search_count([]) > 0,
    )

    end_signature = fields.Html(
        'End signature',
        sanitize=False,
        compute='_compute_end_signature',
    )

    @api.depends('template_id', 'user_email_signature')
    @api.depends_context('uid')
    def _compute_end_signature(self):
        for record in self:
            record.end_signature = record.user_email_signature.signature or self.env.user.signature

    def _compute_body(self):
        super()._compute_body()

        for record in self:
            if record.end_signature and record.body:
                record.body += record.end_signature
