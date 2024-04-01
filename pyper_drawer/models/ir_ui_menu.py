# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    menu_category = fields.Selection(
        selection_add=[
            ('drawer_footer', 'Drawer Footer'),
        ],
    )
