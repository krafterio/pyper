# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def _button_immediate_function(self, function):
        res = super()._button_immediate_function(function)

        if 'ir.global_search.model' in self.env:
            self.env['ir.global_search.model'].sudo()._update_search_models()
        else:
            self.env['ir.model.data'].sudo().search([('module', '=', 'pyper_global_search__model')]).unlink()

        return res

    def _update_translations(self, filter_lang=None, overwrite=False):
        super()._update_translations(filter_lang=filter_lang, overwrite=overwrite)

        if 'ir.global_search.model' in self.env:
            self.env['ir.global_search.model'].sudo()._update_search_models()
