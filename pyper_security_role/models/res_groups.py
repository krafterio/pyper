# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = 'res.groups'

    is_role = fields.Boolean(
        string='Is role?',
        compute='_compute_is_role',
        inverse='_inverse_is_role',
        store=True,
    )

    def _compute_display_name(self):
        super()._compute_display_name()

        if self.env.context.get('display_role_name'):
            for group in self:
                if group.is_role:
                    group.display_name = group.name

    @api.depends('category_id', 'category_id.is_role')
    def _compute_is_role(self):
        for group in self:
            group.is_role = group.category_id.is_role

    def _inverse_is_role(self):
        for group in self:
            if group.is_role and (not group.category_id or not group.category_id.is_role):
                group.category_id = self.env.ref('pyper_security_role.group_security_role')

    @api.onchange('is_role')
    def _onchange_is_role(self):
        self._inverse_is_role()

    def get_application_groups(self, domain):
        """ Return the non-share groups that satisfy ``domain``. """
        return self.search(domain + [('share', '=', False), ('is_role', '=', False)])
