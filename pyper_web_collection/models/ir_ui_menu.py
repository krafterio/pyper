# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    collection_id = fields.Many2one(
        'ir.collections',
        string='Collection',
        ondelete='cascade',
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='cascade',
    )

    shared_user_ids = fields.Many2many(
        'res.users',
        'ir_ui_menu_shared_user_rel',
        'menu_id',
        'user_id',
        string='Users',
        help="if this field is empty, the menu applies to all users. Otherwise, the menu applies to only selected users.",
    )

    def write(self, vals):
        if self.user_id == self.env.user and not self.env.su:
            res = super().sudo().write(vals)
        else:
            res = super().write(vals)

        if self.user_id and self.collection_id:
            for partner in self.user_id.partner_id:
                self.env['bus.bus']._sendone(partner, 'user_menu_collection_changed', {})

        return res

    def unlink(self):
        partner_id = self.user_id.partner_id
        user_menu_collection_changed = bool(self.user_id and self.collection_id)

        res = super().unlink()

        if user_menu_collection_changed:
            for partner in partner_id:
                self.env['bus.bus']._sendone(partner, 'user_menu_collection_changed', {})

        return res
