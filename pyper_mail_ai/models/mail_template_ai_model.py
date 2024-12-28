# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class MailTemplateAiModel(models.Model):
    _name = 'mail.template.ai.model'
    _description = 'Email Template AI Models'

    _sql_constraints = [
        ('unique_model_id', 'UNIQUE(model_id)', 'The model must be unique.')
    ]

    name = fields.Char(
        'Name',
        translate=True,
        related='model_id.name',
        store=True,
    )

    model_id = fields.Many2one(
        'ir.model',
        'Model',
        required=True,
        ondelete='cascade',
    )

    model_name = fields.Char(
        'Model Name',
        related='model_id.model',
        store=True,
    )

    model_information = fields.Html(
        'Information',
        sanitize=False,
        translate=True,
        required=True,
        help='Define the information to use for the selected template',
    )
