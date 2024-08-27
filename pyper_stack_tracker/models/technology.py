# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class Technology(models.Model):
    _name = 'technology'
    _description = 'Technology'
    _order = 'name ASC'

    name = fields.Char(
        'Name'
    )

    code_language_ids = fields.Many2many(
        'code.language',
        'code',
        string='Code languages',
        column1='code_tech',
        column2='technology_code',
    )

    partner_ids = fields.Many2many(
        'res.partner',
        'technology_partner',
        string='Partners',
        column1='partner_id',
        column2='technology_id',
    )

    type_id = fields.Many2one(
        'technology.type',
        'Type',
    )
