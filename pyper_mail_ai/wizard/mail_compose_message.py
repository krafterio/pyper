# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from lxml import etree
from html2text import html2text

from odoo import api, fields, models


class MailComposerMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    use_ai = fields.Boolean(
        related='template_id.use_ai',
    )

    ai_config_id = fields.Many2one(
        related='template_id.ai_config_id',
    )

    ai_model_id = fields.Many2one(
        related='template_id.ai_model_id',
    )

    end_signature = fields.Html(
        'End signature',
        sanitize=False,
    )

    main_partner_id = fields.Many2one(
        'res.partner',
        compute='_compute_main_partner_id',
    )

    prompt = fields.Text(
        compute='_compute_prompts',
    )

    system_prompt_subject = fields.Text(
        compute='_compute_prompts',
    )

    system_prompt_body = fields.Text(
        compute='_compute_prompts',
    )

    @api.depends('partner_ids')
    def _compute_main_partner_id(self):
        for record in self:
            if record.partner_ids:
                record.main_partner_id = record.partner_ids[0]
            else:
                record.main_partner_id = self.env['res.partner']

    @api.depends('template_id', 'main_partner_id')
    def _compute_prompts(self):
        for record in self:
            if not record.use_ai:
                record.system_prompt_subject = False
                record.system_prompt_body = False
                record.prompt = False
                continue

            # Subject
            record.system_prompt_subject = self._generate_prompt(self.ai_config_id.instruction_subject)

            # Body
            record.system_prompt_body = self._generate_prompt(self.ai_config_id.instruction_content)

            # Mail Prompt
            record.prompt = self._generate_prompt(self.template_id.body_html, {'object': record.main_partner_id})

            # Mail Prompt Model Information
            model_info = record.ai_model_id.model_information
            if model_info:
                record.prompt += "\n" + self._generate_prompt(model_info, {'object': record.main_partner_id})

    def _generate_prompt(self, content, variables = None):
        return html2text(self.env['ir.qweb']._render(etree.HTML(content), variables or {})) if content else False

    def _compute_subject(self):
        super()._compute_subject()

        for record in self:
            if not record.use_ai:
                record.subject = False

    def _compute_body(self):
        super()._compute_body()

        for record in self:
            if not record.use_ai:
                record.body = False
