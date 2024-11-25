# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models
from odoo.addons.base.models.ir_module import assert_log_admin_access


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    @assert_log_admin_access
    def button_install(self):
        res = super().button_install()
        self.env['ir.ui.menu'].sudo()._update_root_icons()

        return res

    def button_upgrade(self):
        super().button_upgrade()
        self.env['ir.ui.menu'].sudo()._update_root_icons()
