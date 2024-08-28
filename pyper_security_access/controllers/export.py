# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import json
import operator
from odoo.addons.web.controllers.export import Export, ExcelExport, CSVExport
from odoo.http import request


class AccessExport(Export):
    def fields_get(self, model):
        request.update_context(check_field_access_rights=not request.env.su)
        return super().fields_get(model)


class AccessExcelExport(ExcelExport):
    def base(self, data):
        return super().base(check_export_fields(data))


class AccessCSVExport(CSVExport):
    def base(self, data):
        return super().base(check_export_fields(data))


def check_export_fields(data):
    if request.env.su:
        return data

    check_access_right = request.env['ir.model.fields.access'].check_field_access_right

    params = json.loads(data)
    model, fields = operator.itemgetter('model', 'fields')(params)

    fields = [f for f in fields if check_access_right(model, f.get('name').replace('/', '.'), 'read')]
    params.update({'fields': fields})

    return json.dumps(params)
