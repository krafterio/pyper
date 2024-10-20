# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import re

from odoo import fields, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    font_icon = fields.Char('Font icon')
    font_icon_color = fields.Char('Font icon color')

    category_id = fields.Many2one(
        'ir.ui.menu.category',
        'Category',
        ondelete='restrict',
    )

    category_sequence = fields.Integer(
        'Category sequence',
        related='category_id.sequence',
    )

    position = fields.Selection(
        [
            ('system_tray', 'System Tray'),
        ],
        'Position',
    )

    def write(self, vals):
        res = super().write(vals)

        for item in self:
            # Force remove menu position value if menu item is a sub menu item
            if item.parent_id and item.position:
                item.position = False

            # Force remove category if menu item is used in position or parent is defined
            if item.category_id and (item.parent_id or item.position):
                item.category_id = False

        return res

    def load_web_menus(self, debug):
        menus = super().load_web_menus(debug)

        ids = list(menus.keys())
        ids.remove('root')

        for menu in menus.values():
            name = menu.get('name')

            if self.is_first_character_emoji(name):
                menu.update({
                    'name': re.sub(r'^[\s\uFE0F\u200B-\u200D\u2060-\u206F]*', '', name[1:]),
                    'emojiIcon': name[0],
                })

        menu_values = self.search_read(
            [('id', 'in', ids)],
            fields=['id', 'parent_path', 'position', 'category_id', 'category_sequence', 'font_icon', 'font_icon_color']
        )

        for menu_value in menu_values:
            position = menu_value.get('position')
            category = menu_value.get('category_id')
            parent_path = [int(x) for x in menu_value.get('parent_path').split('/') if x]
            vals = {}

            if position:
                vals['position'] = position

            if parent_path:
                vals['parentPath'] = parent_path

            if menu_value.get('font_icon'):
                vals['fontIcon'] = menu_value.get('font_icon')

            if menu_value.get('font_icon_color'):
                vals['fontIconColor'] = menu_value.get('font_icon_color')

            if category:
                vals['category'] = category
                vals['categorySequence'] = menu_value.get('category_sequence') or False

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
