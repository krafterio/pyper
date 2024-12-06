# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from markupsafe import Markup


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _init_odoobot(self):
        self.ensure_one()
        odoobot_id = self.env['ir.model.data']._xmlid_to_res_id("base.partner_root")
        channel = self.env['discuss.channel'].channel_get([odoobot_id, self.partner_id.id])
        channel.sudo().message_post(body=self._init_odoobot_message(), author_id=odoobot_id, message_type="comment",
                                    subtype_xmlid="mail.mt_comment")
        self.sudo().odoobot_state = 'onboarding_emoji'

        return channel

    def _init_odoobot_message(self):
        return Markup("%s<br/>%s<br/><b>%s</b> <span class=\"o_odoobot_command\">:)</span>") % (
            _("Hello,"),
            _("Odoo's chat helps employees collaborate efficiently. I'm here to help you discover its features."),
            _("Try to send me an emoji")
        )
