# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    technology_ids = fields.Many2many(
        'technology',
        'technology_partner',
        string='Technologies',
        column1='technology_id',
        column2='partner_id',
    )
