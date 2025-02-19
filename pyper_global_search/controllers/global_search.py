# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class GlobalSearch(http.Controller):
    @http.route('/web/global-search', type='json', auth='user', methods=['POST'])
    def global_search(self, search_value):
        icp = request.env['ir.config_parameter'].sudo()
        limit = int(icp.get_param('pyper_global_search.search_limit', '5'))
        results = []
        total = 0
        search_models = request.env['ir.global_search.model'].search([])

        for search_model in search_models:
            if not request.env[search_model.model_name].check_access_rights('read', raise_exception=False):
                continue
            model_result, model_count = self._search_by_model(search_model, search_value, limit)

            if model_result:
                total += model_count
                results.append({
                    'name': search_model.name,
                    'model': search_model.model_name,
                    'actionId': search_model.action_id.id,
                    'searchDomain': self._search_by_model_build_domain(search_model, search_value),
                    'count': model_count,
                    'items': model_result,
                })

        return {
            'results': results,
            'total': total,
        }

    def _search_by_model(self, search_model, search_value: str, limit: int):
        domain = self._search_by_model_build_domain(search_model, search_value)

        items = []
        count = request.env[search_model.model_name].search_count(domain)

        if count:
            items = request.env[search_model.model_name].search_read(domain, self._search_by_model_read_fields(), limit=limit)

        return items, count

    def _search_by_model_build_domain(self, search_model, search_value: str):
        # Add domain of global search model
        domain = list(safe_eval(search_model.domain) if search_model.domain else [])

        operator = 'ilike'
        search_fnames = search_model._rec_names_search or ([search_model._rec_name] if search_model._rec_name else [])
        aggregator = expression.AND
        domains = []

        # Add domain of action window
        if search_model.sudo().action_id.domain:
            domains.append(safe_eval(search_model.sudo().action_id.domain))

        # Add domain of searchable fields
        for field_name in search_fnames:
            # field_name may be a sequence of field names (partner_id.name)
            # retrieve the last field in the sequence
            field = False

            for fname in field_name.split('.'):
                field = search_model._fields[fname]
                search_model = request.env.get(field.comodel_name)

            if field and field.relational:
                # relational fields will trigger a _name_search on their comodel
                domains.append([(field_name, operator, search_value)])
                continue
            try:
                domains.append([(field_name, operator, field.convert_to_write(search_value, search_model))])
            except ValueError:
                pass  # ignore that case if the value doesn't match the field type

        domain += aggregator(domains)

        return domain

    def _search_by_model_read_fields(self):
        return ['display_name']
