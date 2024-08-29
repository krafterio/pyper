# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from typing import List, Dict

from odoo import api, models


class SecuredBase(models.AbstractModel):
    """
    Secure field access rights on all models only in the "check_field_access_rights" context key is True.
    The context key must be defined in each controller route.
    All methods are secured but the following methods do not need to be:
      - Model.name_search()
      - Model.get_metadata()
      - Model.get_property_definition()
      - Model.read_progress_bar()
      - Model.get_field_translations()
      - Model.grouped()
      - Model.filtered_domain()
      - Model.sorted()
      - Model.concat()
      - Model.union()
      - Model.modified()
    """
    _inherit = 'base'

    @api.model
    def default_get(self, fields_list):
        fields_list = check_access_right_field_names(self, fields_list)
        return super().default_get(fields_list)

    def read(self, fields=None, load='_classic_read'):
        fields = check_access_right_field_names(self, fields)
        return super().read(fields, load)

    @api.model
    def load(self, fields, data):
        fields = check_access_right_field_names(self, fields)
        return super().load(fields, data)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        fields = check_access_right_field_names(self, fields)
        groupby = check_access_right_groupby(self, groupby)
        return super().read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        fields = check_access_right_field_names(self, fields)
        return super().search_read(domain, fields, offset, limit, order, **read_kwargs)

    @api.model
    @api.returns('self')
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        field_names = check_access_right_field_names(self, field_names)
        return super().search_fetch(domain, field_names, offset, limit, order)

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        res = super().search_panel_select_range(field_name, **kwargs)

        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right

            if not check_right(self._name, field_name, 'read'):
                res.update({'values': []})

        return res

    @api.model
    def search_panel_select_multi_range(self, field_name, **kwargs):
        res = super().search_panel_select_multi_range(field_name, **kwargs)

        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right

            if not check_right(self._name, field_name, 'read'):
                res.update({'values': []})

        return res

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)

        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right
            field_names = list(res.keys())

            for field_name in field_names:
                if not check_right(self._name, field_name, 'read'):
                    del res[field_name]

        return res

    def fetch(self, field_names):
        field_names = check_access_right_field_names(self, field_names)
        return super().fetch(field_names)

    def export_data(self, fields_to_export):
        if not self.env.su and self.env.context.get('check_field_access_rights'):
            check_right = self.env['ir.model.fields.access'].check_field_access_right
            fields_to_export = [f for f in fields_to_export if check_right(self._name, f.replace('/', '.'), 'read')]

        return super().export_data(fields_to_export)

    def web_read(self, specification: Dict[str, Dict]) -> List[Dict]:
        specification = check_access_right_field_specifications(self, specification)
        return super().web_read(specification)

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False, lazy=True):
        fields = check_access_right_field_names(self, fields)
        groupby = check_access_right_groupby(self, groupby)
        return super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy)

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        specification = check_access_right_field_specifications(self, specification)
        return super().web_search_read(domain, specification, offset, limit, order, count_limit)


def check_access_right_field_names(self, fields):
    if not self.env.su and self.env.context.get('check_field_access_rights'):
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        fields = [f for f in fields if check_right(self._name, f, 'read')]

    return fields


def check_access_right_field_specifications(self, specification):
    if not self.env.su and self.env.context.get('check_field_access_rights'):
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        field_names = list(specification.keys())

        for field_name in field_names:
            if not check_right(self._name, field_name, 'read'):
                del specification[field_name]

    return specification


def check_access_right_groupby(self, groupby):
    if not self.env.su and self.env.context.get('check_field_access_rights'):
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        groupby = [groupby] if isinstance(groupby, str) else groupby
        groupby = [f for f in groupby if check_right(self._name, f, 'read')]

    return groupby
