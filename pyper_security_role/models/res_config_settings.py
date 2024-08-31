# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, Command, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    user_multi_roles = fields.Boolean(
        string='Multiple roles on users',
        help="Enable this option to allow multiple roles to be managed on users"
    )

    @api.model
    def get_values(self):
        res = super().get_values()

        group_user = self.env.ref('base.group_user').sudo()
        group_multi_roles = self.env.ref('pyper_security_role.group_multi_role')

        res.update({
            'user_multi_roles': group_multi_roles in group_user.implied_ids
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        group_user = self.env.ref('base.group_user').sudo()
        group_multi_roles = self.env.ref('pyper_security_role.group_multi_role')

        if self.user_multi_roles:
            group_user.write({'implied_ids': [Command.link(group_multi_roles.id)]})
        else:
            group_user.write({'implied_ids': [Command.unlink(group_multi_roles.id)]})
            group_multi_roles.users = [Command.clear()]
