# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    feedback = fields.Text(
        'Feedback',
    )

    mail_activity_type_icon = fields.Char(
        related='mail_activity_type_id.icon',
    )

    mail_activity_type_name = fields.Char(
        related='mail_activity_type_id.name',
    )

    def _message_format_extras(self, format_reply):
        self.ensure_one()
        vals = super()._message_format_extras(format_reply)
        vals.update({
            'feedback': self.feedback if self.feedback else False,
            'mail_activity_type_icon': self.mail_activity_type_icon,
            'mail_activity_type_name': self.mail_activity_type_name,
        })

        return vals
