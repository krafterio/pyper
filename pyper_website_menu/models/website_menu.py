# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    is_structured_menu = fields.Boolean(
        'Is Structured Menu',
    )

    parent_is_structured_menu = fields.Boolean(
        'Parent is Structured Menu',
        related='parent_id.is_structured_menu',
    )

    structured_menu_columns = fields.Integer(
        'Number of columns',
        help='Override the number of columns in the structured menu defined in theme',
    )

    font_icon = fields.Char('Font icon')

    font_icon_color = fields.Char('Font icon color')

    description = fields.Char(
        'Description',
        translate=True,
    )

    def write(self, values):
        res = super().write(values)

        for menu in self:
            if menu.is_structured_menu and menu.is_mega_menu:
                menu.is_mega_menu = False

            if not menu.is_structured_menu and menu.structured_menu_columns != 0:
                menu.structured_menu_columns = 0

        return res

    @api.onchange('is_structured_menu')
    def _onchange_is_structured_menu(self):
        for menu in self:
            if menu.is_structured_menu and menu.is_mega_menu:
                menu.is_mega_menu = False

            if not menu.is_structured_menu and menu.structured_menu_columns != 0:
                menu.structured_menu_columns = 0
