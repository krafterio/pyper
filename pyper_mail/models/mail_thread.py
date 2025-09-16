# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import _, models
from odoo.exceptions import UserError


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
        notification_messages = messages.filtered(lambda m: m.message_type == 'notification')
        super()._check_can_update_message_content(messages - notification_messages)
        if notification_messages.tracking_value_ids:
            raise UserError(_("Messages with tracking values cannot be modified"))



