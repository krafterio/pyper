# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class CodeLanguage(models.Model):
    _name = 'code.language'
    _description = 'Code language'

    name = fields.Char(
        'Name'
    )

    color = fields.Integer(
        'Color',
    )

    technology_ids = fields.Many2many(
        'technology',
        'code',
        string='Technologies',
        column1='technology_code',
        column2='code_tech',
    )
