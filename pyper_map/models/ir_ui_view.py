# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class IrUIView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(
        selection_add=[
            ('pyper_map', 'Map'),
        ],
    )

    def _is_qweb_based_view(self, view_type):
        return super()._is_qweb_based_view(view_type) or view_type == 'pyper_map'
