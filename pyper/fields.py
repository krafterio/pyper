# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import odoo

from xmlrpc.client import MAXINT


class IntegerFalsable(odoo.fields.Field):
    """ Encapsulates an :class:`int`. """
    type = 'integer'
    column_type = ('int4', 'int4')

    group_operator = 'sum'

    def _get_attrs(self, model_class, name):
        res = super()._get_attrs(model_class, name)
        # The default group_operator is None for sequence fields
        if 'group_operator' not in res and name == 'sequence':
            res['group_operator'] = None
        return res

    def convert_to_column(self, value, record, values=None, validate=True):
        return None if value is False else int(value or 0)

    def convert_to_cache(self, value, record, validate=True):
        if isinstance(value, dict):
            # special case, when an integer field is used as inverse for a one2many
            return value.get('id', None)

        return False if value is False else int(value or 0)

    def convert_to_record(self, value, record):
        return False if value is None else value

    def convert_to_read(self, value, record, use_display_name=True):
        # Integer values greater than 2^31-1 are not supported in pure XMLRPC,
        # so we have to pass them as floats :-(
        if value and value > MAXINT:
            return float(value)
        return value

    def _update(self, records, value):
        # special case, when an integer field is used as inverse for a one2many
        cache = records.env.cache
        for record in records:
            cache.set(record, self, value.id or 0)

    def convert_to_export(self, value, record):
        if value or value == 0:
            return value
        return ''


odoo.fields.IntegerFalsable = IntegerFalsable
