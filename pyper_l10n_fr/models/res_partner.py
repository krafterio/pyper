# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ape = fields.Char(
        'APE'
    )
