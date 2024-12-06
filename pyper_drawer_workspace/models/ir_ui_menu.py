# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    position = fields.Selection(
        selection_add=[
            ('workspace_menu', 'Workspace Menu'),
        ],
    )
