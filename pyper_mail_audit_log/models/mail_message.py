# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    tracking_value_count = fields.Integer(
        'Tracking Value Count',
        compute='_compute_tracking_value_count',
        store=True,
    )

    is_audit_log = fields.Boolean(
        'Is Audit Log',
        compute='_compute_is_audit_log',
        store=True,
    )

    @api.depends('tracking_value_ids')
    def _compute_tracking_value_count(self):
        for message in self:
            message.tracking_value_count = len(message.tracking_value_ids)

    @api.depends('tracking_value_count', 'message_type', 'mail_activity_type_id', 'is_internal')
    def _compute_is_audit_log(self):
        for message in self:
            message.is_audit_log = message.tracking_value_count > 0

    def _message_format_extras(self, format_reply):
        self.ensure_one()
        vals = super()._message_format_extras(format_reply)
        vals.update({
            'is_audit_log': self.is_audit_log,
        })

        return vals

    @api.model
    def _message_fetch(self, domain, search_term=None, before=None, after=None, around=None, limit=30):
        if self.env.context.get('mail_message_without_audit_log', False):
            domain.append(('is_audit_log', '=', False))

        return super()._message_fetch(domain, search_term, before, after, around, limit)
