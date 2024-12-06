# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, Command


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _update_root_hidden_menus(self):
        pass

    def _hidden_menu_ref(self, menu_xmlid: str):
        group_hidden = self.env.ref('pyper_ui_kit.group_hidden', False)

        menu = self.env.ref(menu_xmlid, False)

        if group_hidden and menu:
            menu.groups_id = [Command.set([group_hidden.id])]
