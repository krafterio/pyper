# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PyperTagMixin(models.AbstractModel):
    _name = 'pyper.tag.mixin'
    _description = 'Pyper Tag Mixin'

    tag_ids = fields.Many2many(
        'pyper.tag',
        string='Tags', 
    )

    tag_model_name = fields.Char(
        'Associated tag model name',
        compute='_compute_tag_model_name',
    )

    def _compute_tag_model_name(self):
        for mixin in self:
            mixin.tag_model_name = self._name

    # tag_list = fields.Many2many('pyper.tag', string='Tag list', compute='_compute_tag_list')

    # un compute qui va chercher tous les tag avec tag_model_name self._name .... >_<
    # def _compute_tag_list(self):
    #     self.tag_list = self.env['pyper.tag'].search([
    #         ('tag_model_name', '=', self._name)
    #     ])

    # [!] non utilisé pour le moment
    @api.model
    def create_tag(self, tag_value):
        if self._try_find_tag(tag_value):
            raise UserError(
                _(
                    'A tag with "{value}" value'
                    'already exists for "{tag_model_name}" model'
                ).format(
                    value=tag_value,
                    tag_model_name=self._name,
                )
            )
        return self.env['pyper.tag'].create({
            'value': tag_value,
            'tag_model_name': self._name
        })

    # [!] non utilisé pour le moment
    def add_tag(self, tag_value):
        tag = self._try_find_tag(tag_value)
        if not tag:
            tag = self.create_tag(tag_value)
        self.write({'tag_ids': [(4, tag.id)]})

    # [!] non utilisé pour le moment
    def remove_tag(self, tag_value):
        tag = self._try_find_tag(tag_value)
        if tag:
            self.write({'tag_ids': [(3, tag.id)]})


    # [+] Améliorer la notion de tag unique (privé / public ... par valeur ? ... )
    def _try_find_tag(self, tag_value):
        return self.env['pyper.tag'].search([
            ('value', '=', tag_value),
            ('tag_model_name', '=', self._name)
        ], limit=1)
