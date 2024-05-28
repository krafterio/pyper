# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, tools


class ResUsers(models.Model):
    _inherit = 'res.users'

    organization_id = fields.Many2one(
        'organization',
        compute='_compute_organization_id',
        store=True,
        readonly=False,
    )

    organization_ids = fields.Many2many(
        'organization',
        'organization_users_rel',
        'user_id',
        'oid',
        string='Organizations',
    )

    organizations_count = fields.Integer(
        compute='_compute_organizations_count',
        string="Number of Organizations",
    )

    @api.depends('organization_ids')
    def _compute_organization_id(self):
        for record in self:
            if len(record.organization_ids) > 0:
                record.organization_id = record.organization_ids[0]
            else:
                record.organization_id = self.env['organization']

    @api.depends('company_id')
    def _compute_organizations_count(self):
        self.organizations_count = self.env['organization'].sudo().search_count([])

    @tools.ormcache('self.id', 'self.company_ids', 'self.organization_ids', 'self.env.companies')
    def _get_organization_ids(self):
        # use search() instead of `self.organization_ids` to avoid extra query for `active_test`
        domain = [('active', '=', True), ('user_ids', 'in', self.id)]
        return self.env['organization'].search(domain)._ids
