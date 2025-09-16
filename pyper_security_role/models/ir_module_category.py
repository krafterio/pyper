# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class IrModuleCategory(models.Model):
    _inherit = 'ir.module.category'

    is_role = fields.Boolean(
        string='Is role?',
    )
