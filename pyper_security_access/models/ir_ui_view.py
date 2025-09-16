# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import models


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _postprocess_access_rights(self, tree):
        if not self.env.su:
            self._postprocess_access_rights_fields(tree)

        return super()._postprocess_access_rights(tree)

    def _postprocess_access_rights_fields(self, tree):
        access_right = self.env['ir.model.fields.access']

        for field_node in tree.xpath('//field'):
            if field_node.get('invisible') in ['True', 'true', '1']:
                continue

            config = access_right.get_field_access_rights(self._get_model_name(field_node), field_node.get('name'))

            if not config.get('read'):
                field_node.set('invisible', 'True')
                field_node.set('column_invisible', 'True')

            elif not config.get('write'):
                field_node.set('readonly', 'True')

    def _get_model_name(self, field_node):
        parent_model = field_node.getroottree().getroot().get('model_access_rights')
        parent_field_nodes = get_parent_fields(field_node)

        for parent_field_node in parent_field_nodes:
            parent_fields_info = self.env[parent_model].fields_get()
            parent_field_name = parent_field_node.get('name')

            if parent_field_name in parent_fields_info:
                parent_field_type = parent_fields_info[parent_field_name]['type']

                if parent_field_type in ['many2one', 'one2many', 'many2many']:
                    parent_model = parent_fields_info[parent_field_name]['relation']

        return parent_model

    def _render_template(self, template, values=None):
        values.update({
            'is_granted': self._is_granted,
        })

        return super()._render_template(template, values)

    def _is_granted(self, model: str, field: str, operation: str = 'read') -> bool:
        return self.env['ir.model.fields.access'].check_field_access_right(model, field, operation)


def get_parent_fields(node):
    parents = []
    parent_field_node = node.getparent()

    while parent_field_node is not None:
        if parent_field_node.tag == 'field':
            parents.append(parent_field_node)

        parent_field_node = parent_field_node.getparent()

    parents.reverse()

    return parents
