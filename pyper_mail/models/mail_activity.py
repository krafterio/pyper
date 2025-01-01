# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models

from markupsafe import Markup


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        res = super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

        for model, activity_data in self._classify_by_model().items():
            for message, activity in zip(res[0], activity_data['activities']):
                message.subject = activity.summary
                message.author_id = activity.user_id.partner_id
                message.body = activity.note
                message.feedback = feedback

                if message.mail_activity_type_id and message.mail_activity_type_id.id == self.env.ref('mail.mail_activity_data_email').id:
                    message.message_type = 'email_outgoing'

        return res
