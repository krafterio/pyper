# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class TechnologyType(models.Model):
    _name = 'technology.type'
    _description = 'Technology type'

    name = fields.Char(
        'Name'
    )
