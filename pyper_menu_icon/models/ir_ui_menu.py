# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    font_icon = fields.Char('Font icon')
    font_icon_color = fields.Char('Font icon color')

    menu_category = fields.Selection(
        [
            ('crm', 'CRM'),
            ('sales', 'Sales'),
            ('services', 'Services'),
            ('accounting', 'Accounting'),
            ('stock', 'Stock'),
            ('production', 'Production'),
            ('website', 'Website'),
            ('marketing', 'Marketing'),
            ('hr', 'Human Resources'),
            ('productivity', 'Productivity'),
            ('technic', 'Technic'),
            ('global', 'Global'),
            ('manager', 'Manager'),
            ('system_tray', 'System Tray'),
        ],
        'Menu category',
    )

    def write(self, vals):
        res = super().write(vals)

        for item in self:
            # Force remove menu category value if menu item is a sub menu item
            if item.parent_id and item.menu_category:
                item.menu_category = False

        return res

    def load_web_menus(self, debug):
        menus = super().load_web_menus(debug)

        ids = list(menus.keys())
        ids.remove('root')

        menu_values = self.search_read(
            [('id', 'in', ids)],
            fields=['id', 'font_icon', 'font_icon_color', 'menu_category', 'parent_path']
        )

        for menu_value in menu_values:
            category = menu_value.get('menu_category')
            parent_path = [int(x) for x in menu_value.get('parent_path').split('/') if x]
            vals = {}

            if parent_path:
                vals['parentPath'] = parent_path

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
