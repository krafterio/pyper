# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class MailTemplateAiConfig(models.Model):
    _name = 'mail.template.ai.config'
    _description = 'Email Template AI Configurations'
    _order = 'sequence ASC'

    sequence = fields.Integer(
        'Sequence',
        default=10,
    )

    name = fields.Char(
        'Name',
        required=True,
        translate=True,
    )

    user_model_id = fields.Many2one(
        'ir.model',
        default=lambda self: self.env.ref('base.model_res_users').id,
    )

    user_model_name = fields.Char(
        related='user_model_id.model',
    )

    instruction_content = fields.Html(
        'Content Instruction',
        sanitize=False,
        translate=True,
        required=True,
    )

    instruction_subject = fields.Html(
        'Subject Instruction',
        sanitize=False,
        translate=True,
        required=True,
    )
