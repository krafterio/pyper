# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models

from lxml import etree


class IrQweb(models.AbstractModel):
    _inherit = 'ir.qweb'

    def _get_template(self, template):
        element, document, ref = super()._get_template(template)
        edited = self._postprocess_access_rights(element)

        if edited:
            document = etree.tostring(element, pretty_print=True).decode('utf-8')

        return element, document, ref

    def _postprocess_access_rights(self, tree):
        if self.env.su:
            return False

        edited = False

        for node in tree.xpath('//*[@t-field]'):
            edited = True
            field_name = node.get('t-field')
            field = '.'.join(field_name.split('.')[1:])
            base = field_name.split('.', 1)[0]

            node.set('t-if', 'is_granted(' + base + '._name, "' + field + '") if is_granted else True')

        return edited
