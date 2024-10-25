# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PyperTagMixin(models.AbstractModel):
    _name = 'pyper.tag.mixin'
    _description = 'Pyper Tag Mixin'

    tag_ids = fields.Many2many(
        'pyper.tag',
        string='Tags', #[+] compute avec la valeur du nom générique ?
    )

    @api.model
    def create_tag(self, tag_value):
        if self._try_find_tag(tag_value):
            raise UserError(
                _(
                    'A tag with "{value}" value'
                    'already exists for "{model_name}" model'
                ).format(
                    value=tag_value,
                    model_name=self._name,
                )
            )
        return self.env['pyper.tag'].create({
            'value': tag_value,
            'model_name': self._name
        })

    def add_tag(self, tag_value):
        tag = self._try_find_tag(tag_value)
        if not tag:
            tag = self.create_tag(tag_value)
        self.write({'tag_ids': [(4, tag.id)]})

    def remove_tag(self, tag_value):
        tag = self._try_find_tag(tag_value)
        if tag:
            self.write({'tag_ids': [(3, tag.id)]})

    # [+][!]  a tester pour definir comment appeller / utiliser
    def update_generic_name(self, new_generic_name):
        tags_to_update = self.env['pyper.tag'].search([('model_name', '=', self._name)])
        if tags_to_update:
            tags_to_update.write({'generic_name': new_generic_name})
        else:
            raise UserError('No tag to update with generice name "{}" found'.format(self._name))


    # [+] Améliorer la notion de tag unique (privé / public ... par valeur ? ... )
    def _try_find_tag(self, tag_value):
        return self.env['pyper.tag'].search([
            ('value', '=', tag_value),
            ('model_name', '=', self._name)
        ], limit=1)
