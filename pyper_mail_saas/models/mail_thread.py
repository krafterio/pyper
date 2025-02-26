# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, api


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_auto_subscribe_notify(self, partner_ids, template):
        if template == "mail.message_user_assigned":
            if self.env["ir.config_parameter"].sudo().get_param("pyper.block_all_assignation_mail"):
                return super(MailThread,self.with_context(mail_auto_subscribe_no_notify=True))._message_auto_subscribe_notify(partner_ids,template)
            if self.env["ir.config_parameter"].sudo().get_param("pyper.block_assignation_mail"):
                blocked_models = self.env["ir.config_parameter"].sudo().get_param("pyper.models_to_block")
                blocked_models_ids = blocked_models.split(',') if blocked_models else []
                blocked_models = self.env["ir.model"].sudo().browse([int(model_id) for model_id in blocked_models_ids])
                if self._name in blocked_models.mapped("model"):
                    return super(MailThread,self.with_context(mail_auto_subscribe_no_notify=True))._message_auto_subscribe_notify(partner_ids,template)
        return super()._message_auto_subscribe_notify(partner_ids, template)
