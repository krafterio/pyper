# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import re

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

        for menu in menus.values():
            if self.is_first_character_emoji(menu.get('name')):
                name = menu.get('name')
                menu.update({
                    'name': re.sub(r'^[\s\uFE0F\u200B-\u200D\u2060-\u206F]*', '', name[1:]),
                    'emoji_icon': name[0],
                })

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

    @staticmethod
    def is_first_character_emoji(text):
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]'  # Emoticons (Smileys)
            r'|[\U0001F300-\U0001F5FF]'  # Miscellaneous symbols and pictographs
            r'|[\U0001F680-\U0001F6FF]'  # Transport and map symbols
            r'|[\U0001F700-\U0001F77F]'  # Alchemical symbols and miscellaneous
            r'|[\U0001F780-\U0001F7FF]'  # Geometric shapes
            r'|[\U0001F800-\U0001F8FF]'  # Additional animals and nature
            r'|[\U0001F900-\U0001F9FF]'  # Additional emoticons and hand gestures
            r'|[\U0001FA00-\U0001FA6F]'  # Additional Miscellaneous objects
            r'|[\U0001FA70-\U0001FAFF]'  # Additional miscellaneous symbols
            r'|[\U00002700-\U000027BF]'  # Various symbols (like ★, ✉, etc.)
            r'|[\U000024C2-\U0001F251]'  # Other miscellaneous symbols
            r'|[\U0001F1E0-\U0001F1FF]'  # Flags (regional flag sequence)
            ,
            flags=re.UNICODE
        )

        return bool(emoji_pattern.match(text))
