# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import _, api, fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    use_ai = fields.Boolean(
        'Use AI',
        help='Use AI to write email in email composer',
    )

    ai_config_id = fields.Many2one(
        'mail.template.ai.config',
        'AI Config',
    )

    ai_model_id = fields.Many2one(
        'mail.template.ai.model',
        'AI Model',
    )

    @api.depends('use_ai')
    def _compute_display_name(self):
        super()._compute_display_name()

        for record in self:
            if record.use_ai:
                record.display_name += ' (' + _('with AI') + ')'

    @api.onchange('use_ai')
    def _onchange_use_ai(self):
        for record in self:
            if record.use_ai:
                record.ai_config_id = self.env['mail.template.ai.config'].search([], limit=1)
                record.ai_model_id = self.env['mail.template.ai.model'].search([
                    ('model_id', '=', record.model_id.id),
                ], limit=1)
            else:
                record.ai_config_id = False
                record.ai_model_id = False

    @api.onchange('ai_model_id')
    def _onchange_ai_model_id(self):
        for record in self:
            record.model_id = record.ai_model_id.model_id
