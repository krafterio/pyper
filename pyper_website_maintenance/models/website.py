# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    is_under_maintenance = fields.Boolean(
        string='Under Maintenance',
        help='Enable or disable to show maintenance page',
    )

    under_maintenance_page = fields.Many2one(
        'website.page',
        'Under Maintenance Page',
        help='The published and no indexed website page used to display the maintenance page',
    )
