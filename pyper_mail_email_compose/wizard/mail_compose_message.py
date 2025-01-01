# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class MailComposerMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _prepare_mail_values_static(self):
        res = super()._prepare_mail_values_static()

        if self.env.context.get('mail_email_compose', False):
            res.update({
                'is_internal': True,
                'message_type': 'email_outgoing',
                'subtype_id': self.env.ref('mail.mt_activities').id,
                'mail_activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
                'email_layout_xmlid': 'pyper_user_email_signature.mail_simple_email_layout',
                'email_add_signature': False,
            })

        return res
