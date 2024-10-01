# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    disable_partner_receive_subscribe = fields.Boolean(
        default=lambda self: bool(
            self.env['ir.config_parameter'].sudo().get_param(
                'disable_msg_post_recipients_subscribe'
            )
        ),
        store=False,
    )

    disable_msg_post_self_subscribe = fields.Boolean(
        default=lambda self: bool(
            self.env['ir.config_parameter'].sudo().get_param('disable_msg_post_self_subscribe')
        ),
        store=False,
    )

    subscription_disabled_models = fields.Char(
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('subscription_disabled_models'),
        store=False,
    )

    def get_msg_post_recipients_default_checked(self):
        return bool(self.env['ir.config_parameter'].sudo().get_param(
            'msg_post_recipients_default_checked'
        ))

    def message_subscribe(self, *args, **kwargs):
        if self.subscription_disabled_models and \
           self._name in self.subscription_disabled_models.split(',') and \
           'partner_id' in self and args and self.partner_id.id in args[0]:
            args[0].remove(self.partner_id.id)
        return super().message_subscribe(*args, **kwargs)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *args, **kwargs):
        extra_ctx = {}
        if self.disable_msg_post_self_subscribe:
            extra_ctx['mail_create_nosubscribe'] = True
        if self.disable_partner_receive_subscribe:
            extra_ctx['mail_post_autofollow'] = False
        return super(
            MailThread, self.with_context(**extra_ctx)
        ).message_post(*args, **kwargs)
