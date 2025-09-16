# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from typing import List, Dict

from odoo import api, models


CONTEXT_CHECK_FIELD_ACCESS_RIGHTS = 'check_field_access_rights'
CONTEXT_SKIP_CHECK_FIELD_ACCESS_RIGHTS = 'skip_check_field_access_rights'


class SecuredBase(models.AbstractModel):
    """
    Secure field access rights on all models only in the "check_field_access_rights" context key is True.
    The context key must be defined in each controller route.
    All methods are secured but the following methods do not need to be:
      - Model.copy_data()
      - Model.copy_multi()
      - Model.copy_translations()
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

    def with_field_access_rights(self):
        return self.with_context(**{CONTEXT_CHECK_FIELD_ACCESS_RIGHTS: True}) if not self.env.su else self

    def has_check_field_access_rights(self):
        return (not self.env.su
                and self.env.context.get(CONTEXT_CHECK_FIELD_ACCESS_RIGHTS)
                and not self.env.context.get(CONTEXT_SKIP_CHECK_FIELD_ACCESS_RIGHTS))

    @api.model
    def new(self, values=None, origin=None, ref=None):
        values = check_access_right_map_fields(self, values, operation='write')
        return super().new(values, origin, ref)

    @api.model_create_multi
    def create(self, vals_list):
        if self.has_check_field_access_rights():
            for vals in vals_list:
                check_access_right_map_fields(self, vals, operation='write')
        return super().create(vals_list)

    def update(self, values):
        values = check_access_right_map_fields(self, values, operation='write')
        return super().update(values)

    def update_field_translations(self, field_name, translations):
        access_right = self.env['ir.model.fields.access'].check_field_access_right

        if self.has_check_field_access_rights() and not access_right(self._name, field_name, 'write'):
            translations = {}

        return super().update_field_translations(field_name, translations)

    def write(self, vals):
        vals = check_access_right_map_fields(self, vals, operation='write')
        return super().write(vals)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        _self = self

        if self.has_check_field_access_rights():
            _self = self.with_context(**{CONTEXT_SKIP_CHECK_FIELD_ACCESS_RIGHTS: True})

            if default:
                default = check_access_right_map_fields(_self, default, 'write')

        return super(SecuredBase, _self).copy(default)

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

        if self.has_check_field_access_rights():
            check_right = self.env['ir.model.fields.access'].check_field_access_right

            if not check_right(self._name, field_name, 'read'):
                res.update({'values': []})

        return res

    @api.model
    def search_panel_select_multi_range(self, field_name, **kwargs):
        res = super().search_panel_select_multi_range(field_name, **kwargs)

        if self.has_check_field_access_rights():
            check_right = self.env['ir.model.fields.access'].check_field_access_right

            if not check_right(self._name, field_name, 'read'):
                res.update({'values': []})

        return res

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        res = check_access_right_map_fields(self, res, 'read')
        return res

    def fetch(self, field_names):
        field_names = check_access_right_field_names(self, field_names)
        return super().fetch(field_names)

    def export_data(self, fields_to_export):
        if self.has_check_field_access_rights():
            check_right = self.env['ir.model.fields.access'].check_field_access_right
            fields_to_export = [f for f in fields_to_export if check_right(self._name, f.replace('/', '.'), 'read')]

        return super().export_data(fields_to_export)

    def web_save(self, vals, specification: Dict[str, Dict], next_id=None) -> List[Dict]:
        # Note: 'vals' is filtered by create() or write() methods
        specification = check_access_right_map_fields(self, specification, 'write')
        return super().web_save(vals, specification, next_id)

    def web_override_translations(self, values):
        values = check_access_right_map_fields(self, values, 'write')
        return super().web_override_translations(values)

    def web_read(self, specification: Dict[str, Dict]) -> List[Dict]:
        specification = check_access_right_map_fields(self, specification, 'read')
        return super().web_read(specification)

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False, lazy=True):
        fields = check_access_right_field_names(self, fields)
        groupby = check_access_right_groupby(self, groupby)
        return super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy)

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        specification = check_access_right_map_fields(self, specification, 'read')
        return super().web_search_read(domain, specification, offset, limit, order, count_limit)


def check_access_right_field_names(self, fields):
    fields = [n for n in self._fields] if fields is None else fields
    if self.has_check_field_access_rights():
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        fields = [f for f in fields if check_right(self._name, f, 'read')]

    return fields


def check_access_right_map_fields(self, values, operation='read'):
    if self.has_check_field_access_rights():
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        field_names = list(values.keys())

        for field_name in field_names:
            if not check_right(self._name, field_name, operation):
                del values[field_name]

    return values


def check_access_right_groupby(self, groupby):
    if self.has_check_field_access_rights():
        check_right = self.env['ir.model.fields.access'].check_field_access_right
        groupby = [groupby] if isinstance(groupby, str) else groupby
        groupby = [f for f in groupby if check_right(self._name, f, 'read')]

    return groupby
