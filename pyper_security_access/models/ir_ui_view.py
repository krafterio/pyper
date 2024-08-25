# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class Model(models.AbstractModel):
    _inherit = 'ir.ui.view'

    def _postprocess_access_rights(self, tree):
        model = tree.get('model_access_rights')
        model_field_names = []
        field_nodes = []

        for field_node in tree.xpath('//field'):
            if field_node.get('invisible') in ['True', 'true', '1']:
                continue

            parent_model = model
            parent_field_nodes = self._get_parent_fields(field_node)

            for parent_field_node in parent_field_nodes:
                parent_fields_info = self.env[parent_model].fields_get()
                parent_field_name = parent_field_node.get('name')

                if parent_field_name in parent_fields_info:
                    parent_field_type = parent_fields_info[parent_field_name]['type']

                    if parent_field_type in ['many2one', 'one2many', 'many2many']:
                        parent_model = parent_fields_info[parent_field_name]['relation']

            model_field_names.append((parent_model, field_node.get('name')))
            field_node.set('access_right_key', parent_model + ':' + field_node.get('name'))
            field_nodes.append(field_node)

        map_access_rights = self.env['ir.model.fields.access'].get_access_rights(model_field_names)

        for field_node in field_nodes:
            field_access_key = field_node.get('access_right_key')

            if field_access_key in map_access_rights:
                config = map_access_rights[field_access_key]

                if config.get('perm_invisible'):
                    field_node.set('invisible', 'True')

                elif config.get('perm_read') and not config.get('perm_write'):
                    field_node.set('readonly', 'True')

        return super()._postprocess_access_rights(tree)

    @staticmethod
    def _get_parent_fields(node):
        parents = []
        parent_field_node = node.getparent()

        while parent_field_node is not None:
            if parent_field_node.tag == 'field':
                parents.append(parent_field_node)

            parent_field_node = parent_field_node.getparent()

        parents.reverse()

        return parents
