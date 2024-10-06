# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    requests_count = fields.Integer(string='requests count', compute='_compute_requests_count')
    require_request_approval = fields.Boolean(string='Require request approval', default=False)
    
    def action_validate_request(self):
        self.ensure_one()
        self.require_request_approval = True

    def action_reject_request(self):
        self.ensure_one()
        self.require_request_approval = False

    def action_open_partner_request_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'requests',
            'res_model': 'res.partner.request',
            'view_mode': 'tree,kanban,form',
            'domain': [('author_parent_id', '=', self.id)],
        }

    def _compute_requests_count(self):
        for partner in self:
            partner.requests_count = self.env['res.partner.request'].search_count([('author_parent_id', '=', self.id)])
