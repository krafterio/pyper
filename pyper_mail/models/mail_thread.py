# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _creation_message(self):
        if self._name == 'res.partner':
            self.ensure_one()

            if self.company_type == 'person':
                return _('The contact %s was created', self[self._rec_name])

            return _('The company %s was created', self[self._rec_name])

        return super()._creation_message()

    def _check_can_update_message_content(self, messages):
        messages_notification_ids = []
        for message in messages:
            if message.message_type == 'notification':
                messages_notification_ids.append(message.id)
                message.message_type = 'comment'
        res = super()._check_can_update_message_content(messages)
        for message in messages:
            if message.id in messages_notification_ids:
                message.message_type = 'notification'
        return res



