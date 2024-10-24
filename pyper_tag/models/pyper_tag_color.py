# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class PyperTagColor(models.Model):
    _name = 'pyper.tag.color'
    _description = 'Available colors worn by pyper tags'

    name = fields.Char('Color Name', required=True)
    hex_code = fields.Char('Hex Code', required=True)
