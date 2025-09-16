# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models
from odoo.tools import file_open

import csv


class IrGlobalSearchModel(models.Model):
    _name = 'ir.global_search.model'
    _description = 'Global Search Model'
    _order = 'sequence asc'

    sequence = fields.Integer(
        'Sequence',
        default=lambda self: (self.search([], order='sequence desc', limit=1).sequence or 0) + 1,
        copy=False,
    )

    name = fields.Char(
        string='Name',
        translate=True,
        required=True,
    )

    active = fields.Boolean(
        'Active',
        default=True,
    )

    model_id = fields.Many2one(
        'ir.model',
        'Model',
        required=True,
        ondelete='cascade',
    )

    model_name = fields.Char(
        string='Model Name',
        related='model_id.model',
        store=True,
    )

    domain = fields.Char(
        string='Domain',
        help='Optional domain filtering of the destination data, as a Python expression',
    )

    action_id = fields.Many2one(
        'ir.actions.act_window',
        'Action Window',
        required=True,
        help='Action used to open record details or more search',
    )

    action_id_domain = fields.Binary(
        'Action Domain',
        compute='_compute_action_id_domain',
    )

    @api.depends('model_id')
    def _compute_action_id_domain(self):
        for record in self:
            record.action_id_domain = [('res_model', '=', record.model_name)]

    @api.onchange('model_id')
    def _onchange_model_id(self):
        for record in self:
            record.name = record.model_id.name
            record.action_id = False

    def _update_search_models(self):
        search_models = []
        search_model_names = []
        langs = self.env['res.lang'].search([('active', '=', True)]).mapped('code')

        with file_open('pyper_global_search/data/global_search_models.csv', 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                search_models.append(row)

                if row['model_name'] not in search_model_names:
                    search_model_names.append(row['model_name'])

        installed_models = self.env['ir.model'].search([('model', 'in', search_model_names)])
        installed_model_names = [installed_model.model for installed_model in installed_models]

        for search_model in search_models:
            model_name = search_model['model_name']
            translations = {}
            for key, value in search_model.items():
                if '@' in key and value:
                    field_name = key.split('@')[0]
                    locale = key.split('@')[1]
                    if locale not in translations:
                        translations[locale] = {}

                    translations[locale].update({field_name: value})

            if model_name in installed_model_names:
                rec_xmlid = search_model['xmlid']
                model = self.env['ir.model'].with_context(lang='en_US').search([('model', '=', model_name)], limit=1)
                # External Identifier module names of records must not be the name of the addon, otherwise they are
                # deleted when the addon is updated
                existing_search_model = self.with_context(lang='en_US').env.ref(rec_xmlid, False)

                # Update only translations if search model record exists
                if existing_search_model and isinstance(existing_search_model, IrGlobalSearchModel):
                    existing_search_model.write({'name': search_model.get('name') or model.name})
                    existing_search_model._update_search_model_translations(langs, translations, model)
                    continue

                # Create global search model
                existing_search_model = self.with_context(lang='en_US').create({
                    'sequence': int(search_model.get('sequence', '0')),
                    'name': search_model.get('name') or model.name,
                    'model_id': model.id,
                    'domain': search_model.get('domain', False),
                    'action_id': self.env.ref(search_model.get('action_id', False)).id,
                })
                existing_search_model._update_search_model_translations(langs, translations, model)

                # Create external identifier
                self.env['ir.model.data'].create({
                    'module': rec_xmlid.split('.')[0],
                    'name': rec_xmlid.split('.')[1],
                    'model': existing_search_model._name,
                    'res_id': existing_search_model.id,
                })

    def _update_search_model_translations(self, langs: list, translations: dict[str, dict], model):
        self.ensure_one()

        for lang in langs:
            locale = False
            vals = {}

            if lang in translations:
                locale = translations[lang]
            else:
                general_locale = lang.split('_')[0]

                if general_locale in translations:
                    locale = translations[general_locale]

            if locale:
                # Use translations in CSV
                for field_name, translated_value in locale.items():
                    if hasattr(self, field_name):
                        vals[field_name] = translated_value
            elif lang != 'en_US' or not self.name:
                # Use translations of model
                vals.update({'name': model.with_context(lang=lang).name})

            self.with_context(lang=lang).write(vals)
