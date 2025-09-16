# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

from odoo import models


class IrUiViewCustom(models.Model):
    _inherit = 'ir.ui.view.custom'

    def unlink(self):
        """
        Prevent My dashboard custom views from being deleted upon update.
        """
        if self.ref_id.model_id.model == 'dashboard.board':
            return True
        return super().unlink()
