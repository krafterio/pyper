# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    msg_post_recipients_default_checked = fields.Boolean(
        config_parameter='msg_post_recipients_default_checked',
    )

    disable_msg_post_recipients_subscribe = fields.Boolean(
        config_parameter='disable_msg_post_recipients_subscribe',
    )

    disable_msg_post_self_subscribe = fields.Boolean(
        config_parameter='disable_msg_post_self_subscribe',
    )

    subscription_disabled_models = fields.Char(
        config_parameter='subscription_disabled_models',
    )

    subscription_disabled_model_ids = fields.Many2many(
        'ir.model',
        domain=lambda self: [(
            'model', 'in', self.env['ir.model'].search([
                # Filter models that inherits 'mail.thread'
                (
                    'model',
                    'in',
                    list(self.env['mail.thread.main.attachment']._inherit_children)
                    + list(self.env['mail.thread']._inherit_children)
                ),
            ]).mapped('model')
        )],
        default=lambda self:
            self.env['ir.model'].search([
                (
                    'model',
                    'in',
                    (self.env['ir.config_parameter'].get_param('subscription_disabled_models') or '').split(',')
                )
            ]).mapped('id'),
        inverse='_inverse_subscription_disabled_model_ids',
    )

    def _inverse_subscription_disabled_model_ids(self):
        """ As config_parameters does not accept m2m field,
            we store the fields with a comma separated string into a Char config field """
        for setting in self:
            setting.subscription_disabled_models = ','.join(setting.subscription_disabled_model_ids.mapped('model'))
