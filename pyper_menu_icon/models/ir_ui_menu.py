# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    font_icon = fields.Char('Font icon')
    font_icon_color = fields.Char('Font icon color')

    menu_category = fields.Selection(
        [
            ('global', 'Global'),
            ('manager', 'Manager'),
        ],
        'Menu category',
    )

    def load_web_menus(self, debug):
        menus = super().load_web_menus(debug)

        ids = list(menus.keys())
        ids.remove('root')

        menu_values = self.search_read(
            [('id', 'in', ids), '|', ('font_icon', '!=', False), ('menu_category', '!=', False)],
            fields=['id', 'font_icon', 'font_icon_color', 'menu_category']
        )

        for menu_value in menu_values:
            category = menu_value.get('menu_category')
            vals = {}

            if menu_value.get('font_icon'):
                vals['font_icon'] = menu_value.get('font_icon')

            if menu_value.get('font_icon_color'):
                vals['font_icon_color'] = menu_value.get('font_icon_color')

            if category:
                vals['category'] = category
                vals['category_display_name'] = dict(self._fields['menu_category'].selection).get(category)

            if vals:
                menus.get(menu_value.get('id')).update(vals)

        return menus
