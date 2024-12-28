# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import glob, os
from pathlib import Path

from odoo import api, fields, models, Command
from odoo.modules import get_module_path
from odoo.tools import TranslationImporter


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dashboard_use_spreadsheet_dashboard = fields.Boolean(
        'Use Spreadsheet Dashboard?',
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res['dashboard_use_spreadsheet_dashboard'] = self.sudo()._is_spreadsheet_dashboard_enabled()

        return res

    def set_values(self):
        super().set_values()

        if self.dashboard_use_spreadsheet_dashboard:
            self.sudo()._enable_spreadsheet_dashboard()
        else:
            self.sudo()._disable_spreadsheet_dashboard()

    def _update_spreadsheet_dashboard_settings(self):
        settings = self.env['res.config.settings']

        if settings._is_spreadsheet_dashboard_enabled():
            settings._enable_spreadsheet_dashboard()
        else:
            settings._disable_spreadsheet_dashboard()

    @api.model
    def _is_spreadsheet_dashboard_enabled(self):
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        return group and group.active

    def _enable_spreadsheet_dashboard(self):
        # Unarchive menu items of spreadsheet dashboard
        menu = self.env.ref('spreadsheet_dashboard.spreadsheet_dashboard_menu_root', raise_if_not_found=False)

        if menu:
            menu.active = True

            dashboard_menu = self.env.ref('pyper_dashboard.menu_dashboard_root', raise_if_not_found=False)

            if dashboard_menu:
                menu.parent_id = dashboard_menu
                self._translate_spreadsheet_dashboard_menus(True)

        # Enable security group of spreadsheet dashboard
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.active = True
            group._update_user_groups_view()
            self.env.registry.clear_cache()

    def _disable_spreadsheet_dashboard(self):
        # Archive menu items of spreadsheet dashboard
        menu = self.env.ref('spreadsheet_dashboard.spreadsheet_dashboard_menu_root', raise_if_not_found=False)

        if menu:
            menu.active = False
            menu.parent_id = False
            self._translate_spreadsheet_dashboard_menus(False)

        # Remove spreadsheet dashboard security groups for all users
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.users = [Command.unlink(user.id) for user in group.users]
            group.active = False
            group._update_user_groups_view()
            self.env.registry.clear_cache()

    def _translate_spreadsheet_dashboard_menus(self, active: bool):
        translation_importer = TranslationImporter(self.env.cr, verbose=False)

        if active:
            i18n_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../i18n_extra'))
        else:
            module_path = get_module_path('spreadsheet_dashboard')

            if not module_path:
                return

            i18n_path = os.path.realpath(os.path.join(str(module_path), 'i18n'))

        active_langs = self.env['res.lang'].search([('active', '=', True)]).mapped('code')
        po_files = [Path(f) for f in glob.glob(os.path.join(i18n_path, '*.po'))]

        for po_file in po_files:
            file_lang = po_file.stem

            matching_languages = [lang for lang in active_langs if lang.startswith(file_lang)]

            for lang in matching_languages:
                translation_importer.load_file(str(po_file), lang)

        translation_importer.save(overwrite=True)
